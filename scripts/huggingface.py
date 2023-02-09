import os
import numpy as np
import gradio as gr
from huggingface_hub import model_info, create_repo, create_branch, upload_folder, upload_file
from huggingface_hub.utils import RepositoryNotFoundError, RevisionNotFoundError
from modules import scripts, script_callbacks
from subprocess import getoutput

def run(command):
    out = getoutput(f"{command}")
    return out

def push_folder(folder_from, folder_to, branch, token):
    try:
        repo_exists = True
        r_info = model_info(folder_to, token=token)
    except RepositoryNotFoundError:
        repo_exists = False
    finally:
        if repo_exists:
            print(r_info)
        else:
            create_repo(folder_to, private=True, token=token)
    try:
        branch_exists = True
        b_info = model_info(folder_to, revision=branch, token=token)
    except RevisionNotFoundError:
        branch_exists = False
    finally:
        if branch_exists:
            print(b_info)
        else:
            create_branch(folder_to, branch=branch, token=token)    
    upload_folder(folder_path=folder_from, path_in_repo="", revision=branch, repo_id=folder_to, commit_message=f"folder", token=token)
    return "push folder done!"
 
def push_file(file_from, file_to, file_name, branch, token):
    try:
        repo_exists = True
        r_info = model_info(file_to, token=token)
    except RepositoryNotFoundError:
        repo_exists = False
    finally:
        if repo_exists:
            print(r_info)
        else:
            create_repo(file_to, private=True, token=token)
    try:
        branch_exists = True
        b_info = model_info(file_to, revision=branch, token=token)
    except RevisionNotFoundError:
        branch_exists = False
    finally:
        if branch_exists:
            print(b_info)
        else:
            create_branch(file_to, branch=branch, token=token)    
    upload_file(path_or_fileobj=file_from, path_in_repo=file_name, revision=branch, repo_id=file_to, commit_message=f"file", token=token)
    return "push file done!"   

def on_ui_tabs():     
    with gr.Blocks() as huggingface:
        gr.Markdown(
        """
        ### Push Folder to 🤗 Hugging Face
        folder_from = 🖼 Windows: C:\\Users\\PC\\Desktop\\MyModelFolder 🐧 Linux: /home/user/app/stable-diffusion-webui/my-model-folder<br />
        folder_to = camenduru/mymodel <br />
        branch = main <br />
        token = get from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) new token role=write
        """)
        with gr.Group():
            with gr.Box():
                with gr.Row().style(equal_height=True):
                    text_folder_from = gr.Textbox(show_label=False, max_lines=1, placeholder="folder_from")
                    text_folder_to = gr.Textbox(show_label=False, max_lines=1, placeholder="folder_to")
                    text_folder_branch = gr.Textbox(show_label=False, value="main", max_lines=1, placeholder="branch")
                    text_folder_token = gr.Textbox(show_label=False, max_lines=1, placeholder="🤗 token")
                    out_folder = gr.Textbox(show_label=False)
                with gr.Row().style(equal_height=True):
                    btn_push_folder = gr.Button("Push Folder To 🤗")
            btn_push_folder.click(push_folder, inputs=[text_folder_from, text_folder_to, text_folder_branch, text_folder_token], outputs=out_folder)
        gr.Markdown(
        """
        ### Push File to 🤗 Hugging Face
        file_from = 🖼 Windows: C:\\Users\\PC\\Desktop\\MyModelFolder\\model.ckpt 🐧 Linux: /home/user/app/stable-diffusion-webui/my-model-folder/model.ckpt<br />
        file_to = camenduru/mymodel <br />
        file_name = model.ckpt <br />
        branch = main <br />
        token = get from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) new token role=write
        """)
        with gr.Group():
            with gr.Box():
                with gr.Row().style(equal_height=True):
                    text_file_from = gr.Textbox(show_label=False, max_lines=1, placeholder="file_from")
                    text_file_to = gr.Textbox(show_label=False, max_lines=1, placeholder="file_to")
                    text_file_name = gr.Textbox(show_label=False, max_lines=1, placeholder="file_name")
                    text_file_branch = gr.Textbox(show_label=False, value="main", max_lines=1, placeholder="branch")
                    text_file_token = gr.Textbox(show_label=False, max_lines=1, placeholder="🤗 token")
                    out_file = gr.Textbox(show_label=False)
                with gr.Row().style(equal_height=True):
                    btn_push_file = gr.Button("Push File To 🤗")
            btn_push_file.click(push_file, inputs=[text_file_from, text_file_to, text_file_name, text_file_branch, text_file_token], outputs=out_file)
        gr.Markdown(
        """
        ### 🦒 Colab Run Command
        ```py
        model: wget https://huggingface.co/ckpt/anything-v4.5-vae-swapped/resolve/main/anything-v4.5-vae-swapped.safetensors -O /content/stable-diffusion-webui/models/Stable-diffusion/anything-v4.5-vae-swapped.safetensors
        lora:  wget https://huggingface.co/embed/Sakimi-Chan_LoRA/resolve/main/Sakimi-Chan_LoRA.safetensors -O /content/stable-diffusion-webui/extensions/sd-webui-additional-networks/models/lora/Sakimi-Chan_LoRA.safetensors
        embed: wget https://huggingface.co/embed/bad_prompt/resolve/main/bad_prompt_version2.pt -O /content/stable-diffusion-webui/embeddings/bad_prompt_version2.pt
        vae:   wget https://huggingface.co/ckpt/trinart_characters_19.2m_stable_diffusion_v1/resolve/main/autoencoder_fix_kl-f8-trinart_characters.ckpt -O /content/stable-diffusion-webui/models/VAE/autoencoder_fix_kl-f8-trinart_characters.vae.pt
        zip outputs folder: zip -r /content/outputs.zip /content/stable-diffusion-webui/outputs
        ```
        """)
        with gr.Group():
            with gr.Box():
                command = gr.Textbox(show_label=False, max_lines=1, placeholder="command")
                out_text = gr.Textbox(show_label=False)
                btn_run = gr.Button("run command")
                btn_run.click(run, inputs=command, outputs=out_text)
    return (huggingface, "Hugging Face", "huggingface"),
script_callbacks.on_ui_tabs(on_ui_tabs)
