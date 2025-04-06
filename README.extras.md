# smart-news-organizer

Program that translate text

## Testar program

```bash
cd src
python3 -m smart_news_organizer.program
```

## Upload to PYPI

```bash
pip install --upgrade pkginfo twine packaging

cd src
python -m build
twine upload dist/*
```

## Install from PYPI

The homepage in pipy is https://pypi.org/project/smart-news-organizer/

```bash
pip install --upgrade smart-news-organizer
```

Using:

```bash
smart-news-organizer
```

## Install from source
Installing `smart-news-organizer` program

```bash
git clone https://github.com/trucomanx/SmartNewsOrganizer.git
cd SmartNewsOrganizer
pip install -r requirements.txt
cd src
python3 setup.py sdist
pip install dist/smart_news_organizer-*.tar.gz
```
Using:

```bash
smart-news-organizer
```

## Uninstall

```bash
pip uninstall smart_news_organizer
```
