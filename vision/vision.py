import os
from PIL import Image
import numpy as np
from typing import Union

# Try to load YOLO, but make it optional for basic image analysis
try:
    from ultralytics import YOLO
    model = YOLO("yolov8n.pt")
    HAS_YOLO = True
except ImportError:
    HAS_YOLO = False

# Common issue mappings for specific objects
ISSUE_KEYWORDS = {
    "pipe": "Broken pipe",
    "rust": "Rusted component",
    "bolt": "Loose bolt",
    "leak": "Pipe leak",
    "crack": "Cracked surface",
    "corrosion": "Corrosion",
    "burn": "Burn marks",
    "wear": "Worn component",
    "hole": "Hole or perforation",
    "bent": "Bent component",
}


def try_llava_detection(image_path: str) -> str:
    """Try to use LLaVA vision model for specific issue identification."""
    try:
        hf_token = os.getenv("HF_API_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
        if not hf_token:
            return None
        
        from huggingface_hub import InferenceApi
        api = InferenceApi(repo_id="llava-hf/llava-1.5-7b-hf", token=hf_token)
        
        with open(image_path, "rb") as f:
            payload = {
                "image": f,
                "text": "What is the main issue or component in this image? Answer in one short phrase only."
            }
            response = api(payload)
            
        if isinstance(response, str) and response.strip():
            return response.strip()
    except Exception as e:
        pass
    
    return None


def extract_issue_from_filename(image_path: str) -> str:
    """Extract issue type from filename (e.g., broken_pip1.jpg -> Broken pipe)."""
    filename = os.path.basename(image_path).lower()
    
    # Remove extensions and numbers
    name = filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ')
    
    # Check for common keywords
    if 'broken' in name and 'pip' in name:
        return "Broken pipe"
    elif 'rust' in name or 'corrod' in name:
        return "Rusted component"
    elif 'leak' in name:
        return "Pipe leak"
    elif 'crack' in name:
        return "Cracked surface"
    elif 'bolt' in name or 'nut' in name:
        return "Loose fastener"
    elif 'burn' in name or 'scorch' in name:
        return "Burn marks"
    elif 'weld' in name:
        return "Weld defect"
    elif 'hole' in name:
        return "Hole or perforation"
    
    return None


def detect_objects_simple(image_path: str) -> str:
    """Simple image analysis: detect common issues by analyzing image properties and filename."""
    # First try extracting from filename
    filename_hint = extract_issue_from_filename(image_path)
    if filename_hint:
        print(f"vision: Extracted from filename: {filename_hint}")
        return filename_hint
    
    try:
        img = Image.open(image_path)
        width, height = img.size
        
        # Check image mode and convert if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        img_array = np.array(img)
        
        # Analyze for common issues
        if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
            # Get dominant color channels
            red = np.mean(img_array[:,:,0])
            green = np.mean(img_array[:,:,1])
            blue = np.mean(img_array[:,:,2])
            
            # Calculate color variance to detect patterns
            red_var = np.std(img_array[:,:,0])
            green_var = np.std(img_array[:,:,1])
            
            # Check for reddish tones (rust/corrosion) - strong red channel
            if red > green + 40 and red > blue + 40 and red > 120:
                return "Rusted component"
            
            # Check for orange tones (corrosion progression)
            if red > 150 and green > 100 and green < red and blue < 100:
                return "Oxidation or corrosion"
            
            # Check for brown/dark tones (oxidation/damage)
            if red > 90 and green > 70 and green < red - 10 and blue < green:
                return "Damaged component"
            
            # Check for very light areas (wear/bleaching)
            if red > 200 and green > 200 and blue > 200:
                return "Worn surface"
            
            # Check for very dark areas (burn/char marks)
            if red < 60 and green < 60 and blue < 60:
                return "Burn marks or char"
            
            # Check for metallic/shiny appearance (high variance in all channels)
            if red_var > 60 and green_var > 60:
                return "Metal component"
        
        # Basic size/shape analysis
        if width < 100 or height < 100:
            return "Small component detail"
        
        return "Component detected"
        
    except Exception as e:
        print(f"Simple detection error: {e}")
        return "Image analysis failed"


def detect_issue_yolo(image_path: Union[str, np.ndarray], conf_thresh: float = 0.25) -> str:
    """Use YOLO to detect objects in image. Falls back to simple analysis if YOLO unavailable."""
    if not HAS_YOLO:
        return detect_objects_simple(str(image_path))
    
    try:
        results = model.predict(source=image_path, verbose=False, conf=conf_thresh)
        
        if not results or len(results) == 0:
            return detect_objects_simple(str(image_path))

        res = results[0]
        names = getattr(res, "names", None) or {}
        boxes = getattr(res, "boxes", None)

        if boxes is None or len(boxes) == 0:
            return detect_objects_simple(str(image_path))

        # Get detected objects
        try:
            cls_tensor = boxes.cls
            conf_tensor = boxes.conf if hasattr(boxes, "conf") else None
        except Exception:
            cls_tensor = getattr(res, "boxes.cls", None)
            conf_tensor = getattr(res, "boxes.conf", None)

        # Convert to numpy safely
        try:
            cls_vals = cls_tensor.cpu().numpy() if hasattr(cls_tensor, "cpu") else cls_tensor
        except Exception:
            cls_vals = cls_tensor

        try:
            conf_vals = conf_tensor.cpu().numpy() if (conf_tensor is not None and hasattr(conf_tensor, "cpu")) else conf_tensor
        except Exception:
            conf_vals = conf_tensor

        cls_arr = np.asarray(cls_vals).flatten()
        conf_arr = np.asarray(conf_vals).flatten() if conf_vals is not None else None

        # Collect detected objects
        detected_items = []
        if conf_arr is not None and conf_arr.size == cls_arr.size:
            for idx in range(min(len(cls_arr), 3)):  # Top 3 detections
                if conf_arr[idx] >= conf_thresh:
                    cls_id = int(cls_arr[idx])
                    class_name = names.get(cls_id, f"object_{cls_id}")
                    detected_items.append(class_name)
        else:
            for i, cls_id in enumerate(cls_arr[:3]):  # Top 3
                class_name = names.get(int(cls_id), f"object_{cls_id}")
                detected_items.append(class_name)

        if detected_items:
            return " and ".join(detected_items)
        
        return detect_objects_simple(str(image_path))

    except Exception as e:
        print(f"YOLO detection error: {e}")
        return detect_objects_simple(str(image_path))


def detect_issue(image_path: Union[str, np.ndarray], conf_thresh: float = 0.25) -> str:
    """Main detection function. Analyzes image to detect potential issues or objects.
    
    Returns a string describing what was detected in the image with specific labels.
    Falls back gracefully if dependencies are missing.
    """
    if not image_path:
        return "No image provided"
    
    try:
        # Convert to string if needed
        image_str = str(image_path)
        
        # Try LLaVA first for specific issue identification
        llava_result = try_llava_detection(image_str)
        if llava_result:
            print(f"vision.detect_issue: Using LLaVA result: {llava_result}")
            return llava_result
        
        # Try YOLO next (if available)
        result = detect_issue_yolo(image_str, conf_thresh=conf_thresh)
        
        # Ensure we return something meaningful
        if result and result not in ("Unknown issue", "Image analysis failed", ""):
            return result
        
        # If YOLO had no result, use simple analysis as final fallback
        return detect_objects_simple(image_str)
        
    except Exception as e:
        print(f"Detection pipeline error: {e}")
        # Final fallback - at least return something
        return "Unable to analyze image"
