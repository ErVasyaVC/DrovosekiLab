# ЛАБОРАТОРНАЯ РАБОТА
**«Нахождение плана переработки сахарной свеклы, максимизирующего выход сахара и эвристические стратегии ее решения»**

## Скачивание проекта
```commandline
    git clone https://github.com/ErVasyaVC/DrovosekiLab.git
    cd DrovosekiLab
```
## Запуск проекта через `.exe`
- Запустить файл `main.exe`

## Запуск проекта через `python`
1. Установить все зависимости: 
    ```commandline
        pip install -r requirements.txt 
    ```
2. В папке DrovosekiLab запустить:
    ```commandline
        python3 -m src.main
    ```
   или
    ```commandline
       python -m src.main
    ```

## Перекомпиляция проекта
```commandline
 pyinstaller  --onefile --windowed --icon=icons/icon.ico  --distpath . src/main.py
```