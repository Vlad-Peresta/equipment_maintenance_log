# Equipment Maintenance Log

An equipment maintenance log is a register that organizations use 
to record asset maintenance activities

## Check it out!

[Equipment Maintenance Log deployed to Render](https://equipment-maintenance-log.onrender.com/)

## Installation

Python3 must be already installed

#### Download the code
```angular2html
git clone git@github.com:Vlad-Peresta/equipment_maintenance_log.git
cd py-taxi-service-deploying
```

#### Set Up for Unix, macOS
```angular2html
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Set Up for Windows
```angular2html
python3 -m venv venv
.\env\Scripts\activate
pip3 install -r requirements.txt
```

#### Set Up Database
```angular2html
python3 manage.py makemigrations
python3 manage.py migrate
```

#### Start the app
```angular2html
python manage.py runserver
```

## Features

* Authentication functionality for Worker/User
* Managing workers, tasks and logs directly from website
* Admin panel for advanced management

## Testing website

You can use following superuser for testing website:
* Login: admin.user
* Password: 1qazcde3

## DB Structure
![equipment-maintenance-log](https://user-images.githubusercontent.com/106173314/209444568-48c40234-c891-4609-b611-eae696babaa5.png)

## Project screenshots
![Знімок екрана з 2022-12-24 18-30-31](https://user-images.githubusercontent.com/106173314/209444586-e9e57a4f-2798-400b-8fcd-8dcf3db0f9d7.png)
![Знімок екрана з 2022-12-24 18-35-16](https://user-images.githubusercontent.com/106173314/209444601-10a0b796-7499-4c2d-92a2-48321ec52b84.png)
![Знімок екрана з 2022-12-22 22-33-04](https://user-images.githubusercontent.com/106173314/209444611-e68f7564-5c83-46cc-8a3e-fbb39368ee81.png)
![Знімок екрана з 2022-12-22 22-33-22](https://user-images.githubusercontent.com/106173314/209444625-33918cca-b9d5-484c-ba1a-391c002c3e4e.png)
![Знімок екрана з 2022-12-22 22-34-15](https://user-images.githubusercontent.com/106173314/209444627-9c6c844e-0958-49e0-a11a-318f0da295d9.png)
![Знімок екрана з 2022-12-22 22-35-43](https://user-images.githubusercontent.com/106173314/209444633-0e8d8c4f-4883-4fe1-aa2d-7f5fad1557b2.png)
![Знімок екрана з 2022-12-22 22-36-57](https://user-images.githubusercontent.com/106173314/209444634-1599b626-2518-4e25-a57b-4239e1383405.png)
![Знімок екрана з 2022-12-22 22-37-58](https://user-images.githubusercontent.com/106173314/209444637-75f5c590-161b-4d39-9811-e9d6d065920a.png)
![Знімок екрана з 2022-12-22 22-38-33](https://user-images.githubusercontent.com/106173314/209444643-4cc9480a-3647-491d-8ccf-c1b245582c0f.png)
![Знімок екрана з 2022-12-22 22-38-55](https://user-images.githubusercontent.com/106173314/209444650-dd0141e3-b3f6-4569-aee2-01fda72c712d.png)
![Знімок екрана з 2022-12-22 22-39-20](https://user-images.githubusercontent.com/106173314/209444660-739974aa-958c-4bd3-ae6d-71a138611c4f.png)
![Знімок екрана з 2022-12-22 22-39-37](https://user-images.githubusercontent.com/106173314/209444663-e714639e-4c39-4c93-8a5b-a3cc6c871c28.png)
![Знімок екрана з 2022-12-22 22-39-56](https://user-images.githubusercontent.com/106173314/209444667-aaff83c5-f1e7-4b4c-a7c6-51da0f77b877.png)
