import modules.scripts as scripts
import modules.processing as processing
import modules.images as images
import modules.shared as shared
import gradio as gr
import json
import os

class Script(scripts.Script):
    def title(self):
        return "sd-batch-iterator"

    def show(self, is_img2img):
        return True

    def ui(self, is_img2img):
        # UI for the script
        # Changed to File upload to avoid path parsing errors (URLError)
        json_file = gr.File(label="Upload JSON File", file_types=[".json"])
        return [json_file]

    def run(self, p, json_file):
        if json_file is None:
            print("[sd-batch-iterator] No file uploaded.")
            return processing.Processed(p, [], p.seed, "No file uploaded")
            
        # Gradio File component returns a temp file path in 'name' attribute or just the path string depending on version
        # In most recent WebUI versions, it returns a temp file path string if type is default (file) or filepath
        
        json_file_path = json_file.name if hasattr(json_file, 'name') else json_file

        if not os.path.exists(json_file_path):
            print(f"[sd-batch-iterator] File not found: {json_file_path}")
            return processing.Processed(p, [], p.seed, "File not found")

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"[sd-batch-iterator] Error loading JSON: {e}")
            return processing.Processed(p, [], p.seed, f"Error loading JSON: {e}")

        base_prompt = data.get("base_prompt", "")
        variable_prompts = data.get("variable_prompts", [])
        
        # Store original settings
        original_prompt = p.prompt
        original_do_not_save_samples = p.do_not_save_samples
        original_do_not_save_grid = p.do_not_save_grid
        
        # Disable default saving to handle it manually
        p.do_not_save_samples = True
        p.do_not_save_grid = True
        
        all_images = []

        print(f"[sd-batch-iterator] Found {len(variable_prompts)} variations.")

        try:
            for i, variation in enumerate(variable_prompts):
                var_name = variation.get("name", f"var_{i}")
                var_prompt = variation.get("prompt", "")
                
                # Construct new prompt
                full_prompt = f"{base_prompt}, {var_prompt}"
                p.prompt = full_prompt
                
                print(f"[sd-batch-iterator] Processing {i+1}/{len(variable_prompts)}: {var_name}")
                
                # Process images
                proc = processing.process_images(p)
                
                # Save each image with custom suffix
                if proc.images:
                    for img in proc.images:
                        # We use the seed from the processed image for accurate metadata
                        # The suffix dictates the filename
                        images.save_image(
                            img,
                            p.outpath_samples,
                            "",
                            proc.seed,
                            proc.prompt,
                            shared.opts.samples_format,
                            info=proc.info,
                            p=p,
                            suffix=f"-{var_name}"
                        )
                        all_images.append(img)
        finally:
            # Restore original settings
            p.prompt = original_prompt
            p.do_not_save_samples = original_do_not_save_samples
            p.do_not_save_grid = original_do_not_save_grid
        
        return processing.Processed(p, all_images, p.seed, proc.info if all_images else "")
