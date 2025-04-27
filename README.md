# voice2voice

A basic voice to voice built in an hour. Shitty UI though

# Install

```bash
git clone https://github.com/sahildhull/voice2voice.git
cd voice2voice
python3 -m venv venv
source venv/bin/activate
pip install -r req.txt
```

# Run

Terminal 1:
```bash
hypercorn main:app --bind 0.0.0.0:5002 --reload
```

Terminal 2:
```bash
python3 -m http.server 3000
```

Browser: http://localhost:3000
