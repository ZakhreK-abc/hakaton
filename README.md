# hakaton

для запуска сервиса нужно:
1.клонирвать репозиторий
2.перейти в каталог клонированого репозитория
3.создать виртуальное окружение пайтон командой "python -m venv venv" bkb "python3 -m venv venv" в каталоге hakaton
4.активировать виртуально окружение пайтон командой "source venv/bin/activate" на линукс или ".\venv\Scripts\activate" из каталога hakaton
5.установить библиотеки из файла "requirements.txt" командой "pip install -r requirements.txt" или "pip3 install -r requirements.txt"из каталога hakaton
6.запустить api сервер командой "uvicorn app.main:app --reload" из каталога hakaton
7.запустить веб сайт командой "python app.py" находясь в каталоге web
8.перейдите на веб сайт по ip адресу 127.0.0.1:5000