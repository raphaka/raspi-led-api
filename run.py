from led_api import app

if __name__ == "__main__":
    app.run() #use_reloader=False)


#TODO
#auto start pigpiod and exit, if not running
#set different dev Environments, which enable/disable gpio
#check if sending exit to localhost still works for stopping stream mode
#general error handling
#general python naming conventions refactoring PEP8
#add settings page
#add effect (list of dict) number, name, json
#[
#    {'color':'00ff00', 'duration':500, 'fade':True},
#    {''}
#]
#add to effect (update json in db)
#delete effect
#delete from effect
