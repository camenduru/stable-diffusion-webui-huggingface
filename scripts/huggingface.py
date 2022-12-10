import os
import numpy as np
import gradio as gr
from huggingface_hub import model_info, create_repo, create_branch, upload_folder
from huggingface_hub.utils import RepositoryNotFoundError, RevisionNotFoundError
from modules import scripts, script_callbacks

def push_ckpt(model_from, model_to, token, branch):
    try:
        repo_exists = True
        r_info = model_info(model_to, token=token)
    except RepositoryNotFoundError:
        repo_exists = False
    finally:
        if repo_exists:
            print(r_info)
        else:
            create_repo(model_to, private=True, token=token)
    try:
        branch_exists = True
        b_info = model_info(model_to, revision=branch, token=token)
    except RevisionNotFoundError:
        branch_exists = False
    finally:
        if branch_exists:
            print(b_info)
        else:
            create_branch(model_to, branch=branch, token=token)    
    upload_folder(folder_path=model_from, path_in_repo="", revision=branch, repo_id=model_to, commit_message=f"ckpt", token=token)
    return "push folder done!"
    

def on_ui_tabs():     
    with gr.Blocks() as huggingface:
        gr.Markdown(
        """
        ### Push Folder to 🤗 Hugging Face
        ckpt_model_from = 🖼 Windows: C:\\Users\\PC\\Desktop\\MyModelFolder 🐧 Linux: /home/user/app/stable-diffusion-webui/my-model-folder<br />
        ckpt_model_to = camenduru/mymodel <br />
        branch = main <br />
        token = get from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) new token role=write
        """)
        with gr.Group():
            with gr.Box():
                with gr.Row().style(equal_height=True):
                    text_ckpt_model_from = gr.Textbox(show_label=False, max_lines=1, placeholder="ckpt_model_from")
                    text_ckpt_model_to = gr.Textbox(show_label=False, max_lines=1, placeholder="ckpt_model_to")
                    text_ckpt_branch = gr.Textbox(show_label=False, value="main", max_lines=1, placeholder="ckpt_branch")
                    text_ckpt_token = gr.Textbox(show_label=False, max_lines=1, placeholder="🤗 token")
                    out_ckpt = gr.Textbox(show_label=False)
                with gr.Row().style(equal_height=True):
                    btn_push_ckpt = gr.Button("Push Folder To 🤗")
            btn_push_ckpt.click(push_ckpt, inputs=[text_ckpt_model_from, text_ckpt_model_to, text_ckpt_token, text_ckpt_branch], outputs=out_ckpt)
    return (huggingface, "Hugging Face", "huggingface"),
script_callbacks.on_ui_tabs(on_ui_tabs)
