import launch

if not launch.is_installed("huggingface-hub"):
    launch.run_pip("install huggingface-hub==0.11.1", "requirements for push to hugging face extension")