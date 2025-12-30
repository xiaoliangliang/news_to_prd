# Demo 4: Grammar Check Forum

A forum demo where a `grammar-checker` agent automatically replies to new topics and comments with grammar and style suggestions.

## Quick Start

### 0) (Windows) Fix UTF-8 Console Output

If `openagents` crashes with a `UnicodeEncodeError` on Windows terminals, run this once per terminal:

```powershell
$env:PYTHONUTF8=1
$env:PYTHONIOENCODING="utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [Console]::OutputEncoding
```

### 1) Start the Network

```bash
cd demos/04_grammar_check_forum
openagents network start network.yaml
```

### 2) Launch the Agent

In a separate terminal:

```bash
openagents agent start agents/grammar_checker.yaml
```

### 3) Open Studio

```bash
openagents --no-banner studio -s
```

Then open the Studio URL (printed in the terminal), connect to `localhost:8700`, and try creating a topic with intentional grammar issues.

## Notes

- Ports default to HTTP `8700` and gRPC `8600`. If you change them in `network.yaml`, also update `agents/grammar_checker.yaml`.
- Default model is `glm-4.7` in `agents/grammar_checker.yaml`; change it to whatever model you have configured.
