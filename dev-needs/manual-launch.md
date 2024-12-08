# Instructions for Manual Launch

### Download Key

Download the .pem file located in the dev-needs folder - finalproject-group39-vm-webserver_key.pem. Store it somewhere
secure on your machine.

### SSH Into our VM

Execute the following command from your terminal. Be sure to replace "your-filepath" with the location of the key on your
machine.

```
ssh -i "your-filepath\finalproject-group39-vm-webserver_key.pem" azureuser@52.247.248.246
```

### Run the Web App

Once in the VM, you can run our web app via the following commands.

```
cd app
python3 app.py
```

After which, the app will run at http://52.247.248.246:5000/

> ### Other Tips
> 
> You may be prompted for SQL Server credentials. If so, they are given below.
> 
> User: ***finalprojectadmin***
> 
> Password: ***group39SECRET***
