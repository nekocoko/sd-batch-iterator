import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class PromptEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("sd-batch-iterator - 프롬프트 편집기")
        self.root.geometry("800x600")
        
        # Data
        self.current_filepath = None
        self.variations = [] # List of dicts: {'name': '...', 'prompt': '...'}

        # Style
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TLabel", padding=6)

        # === Top Menu Bar ===
        menu_frame = ttk.Frame(root, padding="10")
        menu_frame.pack(fill=tk.X)
        
        ttk.Button(menu_frame, text="JSON 불러오기", command=self.load_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(menu_frame, text="JSON 저장하기", command=self.save_json).pack(side=tk.LEFT, padx=5)
        ttk.Button(menu_frame, text="새로 만들기 / 초기화", command=self.clear_all).pack(side=tk.LEFT, padx=5)

        # === Main Content ===
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Base Prompt Section ---
        ttk.Label(main_frame, text="기본 프롬프트 (공통)").pack(anchor=tk.W)
        self.base_prompt_text = tk.Text(main_frame, height=5, width=50)
        self.base_prompt_text.pack(fill=tk.X, pady=(0, 10))

        # --- Variations Section (Split View) ---
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Left: List/Treeview
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="변동 프롬프트 목록").pack(anchor=tk.W)
        
        # Treeview columns
        self.tree = ttk.Treeview(left_frame, columns=("Enabled", "Name", "Prompt"), show="headings")
        self.tree.heading("Enabled", text="사용")
        self.tree.heading("Name", text="이름 (접미사)")
        self.tree.heading("Prompt", text="프롬프트")
        self.tree.column("Enabled", width=50, anchor="center")
        self.tree.column("Name", width=150)
        self.tree.column("Prompt", width=300)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Select All / Deselect All Buttons
        sel_btn_frame = ttk.Frame(left_frame)
        sel_btn_frame.pack(fill=tk.X, pady=2)
        ttk.Button(sel_btn_frame, text="전체 선택", command=self.select_all).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        ttk.Button(sel_btn_frame, text="전체 해제", command=self.deselect_all).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=1)
        
        # Right: Editor
        right_frame = ttk.Frame(paned_window, padding=(10, 0, 0, 0))
        paned_window.add(right_frame, weight=1)

        ttk.Label(right_frame, text="항목 편집").pack(anchor=tk.W)
        
        # Enabled Checkbox
        self.var_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(right_frame, text="사용함 (Enable)", variable=self.var_enabled).pack(anchor=tk.W, pady=(0, 5))

        # Name Input
        ttk.Label(right_frame, text="이름 (파일명 접미사)").pack(anchor=tk.W)
        self.var_name_entry = ttk.Entry(right_frame)
        self.var_name_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Prompt Input
        ttk.Label(right_frame, text="변동 프롬프트 내용").pack(anchor=tk.W)
        self.var_prompt_text = tk.Text(right_frame, height=10, width=30)
        self.var_prompt_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Action Buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="추가 / 수정", command=self.add_update_variation).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Button(btn_frame, text="선택 삭제", command=self.delete_variation).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def clear_all(self):
        self.base_prompt_text.delete("1.0", tk.END)
        self.variations = []
        self.current_filepath = None
        self.clear_editor_fields()
        self.refresh_tree()
        self.root.title("sd-batch-iterator - 프롬프트 편집기 (새 파일)")

    def clear_editor_fields(self):
        self.var_enabled.set(True)
        self.var_name_entry.delete(0, tk.END)
        self.var_prompt_text.delete("1.0", tk.END)
        # Deselect tree
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection()[0])

    def refresh_tree(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Re-populate
        for i, var in enumerate(self.variations):
            enabled_str = "O" if var.get('enabled', True) else "X"
            self.tree.insert("", "end", iid=str(i), values=(enabled_str, var.get('name', ''), var.get('prompt', '')))

    def select_all(self):
        for var in self.variations:
            var['enabled'] = True
        self.refresh_tree()

    def deselect_all(self):
        for var in self.variations:
            var['enabled'] = False
        self.refresh_tree()

    def load_json(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if not filepath:
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.clear_all()
            self.current_filepath = filepath
            self.root.title(f"sd-batch-iterator - 프롬프트 편집기 ({os.path.basename(filepath)})")
            
            self.base_prompt_text.insert("1.0", data.get("base_prompt", ""))
            self.variations = data.get("variable_prompts", [])
            
            # Ensure enabled field exists
            for var in self.variations:
                if 'enabled' not in var:
                    var['enabled'] = True

            self.refresh_tree()
            
        except Exception as e:
            messagebox.showerror("오류", f"파일을 불러오는데 실패했습니다:\n{e}")

    def save_json(self):
        data = {
            "base_prompt": self.base_prompt_text.get("1.0", tk.END).strip(),
            "variable_prompts": self.variations
        }
        
        if self.current_filepath:
            filepath = self.current_filepath
        else:
            filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
            if not filepath:
                return
            self.current_filepath = filepath
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            self.root.title(f"sd-batch-iterator - 프롬프트 편집기 ({os.path.basename(filepath)})")
            messagebox.showinfo("성공", "파일이 성공적으로 저장되었습니다!")
        except Exception as e:
            messagebox.showerror("오류", f"파일을 저장하는데 실패했습니다:\n{e}")

    def on_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        index = int(selected_items[0])
        var = self.variations[index]
        
        # Populate editor
        self.var_enabled.set(var.get('enabled', True))
        self.var_name_entry.delete(0, tk.END)
        self.var_name_entry.insert(0, var.get('name', ''))
        
        self.var_prompt_text.delete("1.0", tk.END)
        self.var_prompt_text.insert("1.0", var.get('prompt', ''))

    def add_update_variation(self):
        name = self.var_name_entry.get().strip()
        prompt = self.var_prompt_text.get("1.0", tk.END).strip()
        enabled = self.var_enabled.get()
        
        if not name or not prompt:
            messagebox.showwarning("주의", "이름과 프롬프트를 모두 입력해주세요.")
            return

        selected_items = self.tree.selection()
        
        new_item = {"name": name, "prompt": prompt, "enabled": enabled}

        if selected_items:
            # Update existing
            index = int(selected_items[0])
            self.variations[index] = new_item
        else:
            # Add new
            self.variations.append(new_item)
            # Select the new item (optional, but good UX)
        
        self.refresh_tree()
        self.clear_editor_fields()

    def delete_variation(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        if messagebox.askyesno("확인", "선택한 항목을 삭제하시겠습니까?"):
            index = int(selected_items[0])
            del self.variations[index]
            self.refresh_tree()
            self.clear_editor_fields()

if __name__ == "__main__":
    root = tk.Tk()
    app = PromptEditorApp(root)
    root.mainloop()
