from datetime import date, datetime, timedelta
from prettytable import PrettyTable
from pathlib import Path
import csv

def get_last_plant_id():
    count = 0
    try:
        with open('plants.csv','r') as file:
            reader = csv.reader(file, delimiter =',')
            for l in reader:
                count += 1
                last_id = l[0]
            
    except:
        print('No plants file master tracker was found or something went wrong!')
        return(0) # Not file and no headers written in the file... 
    
    if count == 1: # headers available but no data in file..
        return(1)
    else:
        return(int(last_id)+1)

def get_last_activity_id():
    count = 0
    try:
        with open('activity.csv','r') as file:
            reader = csv.reader(file, delimiter =',')
            for l in reader:
                count += 1
                last_id = l[1]
            
    except:
        print('No plants file master tracker was found or something went wrong!')
        return(0)
    
    if count == 1:
        return(1)
    else:
        return(int(last_id)+1)

def get_non_empty(prompt):
    
    while True:
        user_input = input(prompt).strip()
        
        if user_input:
            return(user_input)
        else:
            print('Input cannot be empty.')

    
def add_new_plant():

#Plant name

#I removed typecasting str because it is already string

    # old code to get plant name
    # plant_name = input('Enter Plant name: ').strip()
    #improved code
    plant_name = get_non_empty('Enter Plant name: ')
#old code to get home location
    #home_location = input('Enter the plant location: ').strip()
    #improved code to get home location
    home_location = get_non_empty('Enter the plant location: ')
    
#Date aquired

    while True:
        date_aquired = input("Enter date aquired (YYYY-MM-DD) or press Enter for today: ")
        if not date_aquired.strip():  # Use today's date
            date_aquired = date.today().strftime("%Y-%m-%d")
            break
        try:
            datetime.strptime(date_aquired, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD:")

#water frequency

    while True:
        try:
            water_frequency = int(input("Enter number of days required to water: ").strip())
            if water_frequency > 0:
                break
            else:
                print("Please enter a positive number:")
        except ValueError:
            print("Please enter a valid number:")



#Sunlight needs
    while True:
        print("Enter the sunlight strength needed (From 1 - 3) :\n")
        print("1- Low")
        print("2- Medium")
        print("3- High")

        try:
            sunlight_needed = int(input().strip())
            if sunlight_needed > 0 and sunlight_needed < 4:
                break
            else:
                print("Please enter a number from 1 to 3.")
        except:
            print("Please enter a number from 1 to 3.")
        
    if sunlight_needed == 1:
        sunlight_needed = 'Low'
    elif sunlight_needed == 2:
        sunlight_needed = 'Medium'
    else:
        sunlight_needed = 'High'
        
    
    plant_id = get_last_plant_id()

    
    fieldnames = ['Plant ID','Plant Name','Home Location','Date Acquired','Watering Frequency','Sunlight Needs','Image Path']
    with open('plants.csv','a',newline='\n') as plantsfile:
        writer= csv.DictWriter(plantsfile, fieldnames = fieldnames)
        
        if plant_id == 0:
            plant_id +=1
            writer.writeheader()
        
        writer.writerow({'Plant ID' : plant_id,'Plant Name':plant_name,'Home Location':home_location,'Date Acquired':date_aquired,'Watering Frequency':water_frequency,'Sunlight Needs':sunlight_needed})
    
    print(f'{plant_name} added successfully to plants tracker master file')
    return()


def record_activity():
    print('Here is all the plants. Please choose the plant and enter its ID')
    view_all_plants()
    while True:
        try:
            plant_id = int(input('\n\nEnter the ID (Numbers) of the plant you want to log the activity:').strip())
        
        except:
            print('Please read through the list and enter correct ID (Numbers)')
            continue

        #Below code to verify that what entered is real plant available. Avoiding recording activity for non existing plant
        temp_list=[]
        with open('plants.csv','r') as file:
            reader = csv.reader(file, delimiter=',')
            c = 0
            for l in reader:
                if c == 0:
                    c = 1
                    continue
                temp_list.append(int(l[0]))
        
        
        
        if  plant_id in temp_list:
            break
        else:
            print('Please read the list and enter correct ID')
            
    ################ end of validiation 
    
    
    while True:
        print("Enter the activity which was performed (From 1 - 4) :\n")
        print("1- Watering")
        print("2- Fertilizing")
        print("3- Repotting")
        print("4- Pruning")

        try:
            activity_type = int(input())
            if activity_type > 0 and activity_type < 5:
                break
            else:
                print("Please enter a number from 1 to 4.")
        except:
            print("Please enter a number from 1 to 4.")
        
    if activity_type == 1:
        activity_type = 'Watering'
    elif activity_type == 2:
        activity_type = 'Fertilizing'
    elif activity_type == 3:
        activity_type = 'Repotting'
    else:
        activity_type = 'Pruning'
    ########################
        
    fieldnames = ['Plant ID','Activity ID','Activity','Date Completion']
    last_activity_id = get_last_activity_id() 
    date_completed = date.today().strftime("%Y-%m-%d")
    try:
        with open('activity.csv','a', newline='\n') as fileactivity:
            writer = csv.DictWriter(fileactivity, fieldnames)
            if last_activity_id == 0:
                last_activity_id += 1
                writer.writeheader()
            writer.writerow({'Plant ID':plant_id,'Activity ID':last_activity_id,'Activity':activity_type,'Date Completion':date_completed})
                
    except:
        print('File could not be opened. Contact the support line')
        return (0)
                 
    return()


def search_plants():
    #search_term = input('Please enter the plant name or location: ')
    search_term = get_non_empty('Please enter the plant name or location: ')
    fieldnames = ['Plant ID','Plant Name','Home Location','Date Acquired','Watering Frequency','Sunlight Needs','Image Path','Last Activity','Date Completion']
    
    t = PrettyTable(fieldnames)

    found = 0
    temp_list=[]
    cur_activity = ''
    with open('plants.csv','r') as readfile:
        reader = csv.reader(readfile, delimiter =',')

        for row in reader:

            if row[1].lower() == search_term.lower() or row[2].lower() == search_term.lower():
                temp_list = row
                found += 1
                date1 = datetime.strptime(row[3],"%Y-%m-%d")
                with open('activity.csv','r') as readactivity:
                    reader2 = csv.reader(readactivity, delimiter =',')
                    for line in reader2:
                        if line[1].lower() == row[0].lower():
                            cur_activity = line[2]
                            cur_date = datetime.strptime(line[3], "%Y-%m-%d")
                            if cur_date >= date1:
                                date1 = cur_date
                            
                    temp_list.append(cur_activity)
                    temp_list.append(date1)
                    t.add_row(temp_list)    
                        
    if found >0:
        print(t)
    elif found ==0:
        print("Nothing found by that words. You can view all plants instead")
    
    return()
            


    
def show_menu():
        print("Please enter the number selecting one of the functions below:\n")
        print("1- Add a new plant to the collection")
        print("2- Record a plant care activity")
        print("3- View plants due for care")
        print("4- Search plants by name or location")
        print("5- View all plants")
        print("6- Seasonal Change")
        print("7- Add image")
        print("8- Exit program")


def main():
    
    
    while True:

        show_menu()
        option = input("\nChoose an option: ").strip()
    
        try:
            option = int(option)
        
        except:
            print("Sorry.. something went wrong.")
            continue
        if option < 0  or option > 8:
            print("Sorry! Please enter a value from the above menu")
            continue    
    
        if option == 1:
            add_new_plant()
        elif option == 2:
            record_activity()
        elif option == 3:
            view_plants_due()
        elif option == 4:
            search_plants()
        elif option == 5:
            view_all_plants()
        elif option == 6:
            seasonal_change()
        elif option == 7:
            add_image_path()
        else:
            print("Thank you for using Plant Care Tracker!\nGood Bye :)")
            break #Used break as quit() is not good for Jupyter Notebook..
    

def view_all_plants():
    fieldnames = ['Plant ID','Plant Name','Home Location','Date Acquired','Watering Frequency','Sunlight Needs','Image Path']
    t = PrettyTable(fieldnames)
    first_line = -1
    try:
        with open('plants.csv','r') as file:
            reader = csv.reader(file, delimiter =',')
            for l in reader:
                if first_line == -1:
                    first_line = 0
                    continue
                t.add_row(l)
    except:
        print('No plants file master tracker was found')
        return(0)
    
    print(t)
    
    return()
    
def view_plants_due():
    date_str1 = '1970-01-01'
    date_obj1 = datetime.strptime(date_str1, '%Y-%m-%d')
    # for testing
    table = PrettyTable()
    table.field_names = ['plant ID','Watering Frequency','Date Completed','Status']
    count_p = -1
    temp_list=[]
    with open('plants.csv','r') as plantsfile:
        readerplants = csv.reader(plantsfile, delimiter =',')
        for line in readerplants:
            if count_p != -1:
                plant_id = line[0]
                watering_frequency = line[4]
                date_obj1 = datetime.strptime(line[3][0:10], '%Y-%m-%d')
            else:    
                count_p = 1
                continue
                
            count_a = -1
            attention = ''
            with open('activity.csv','r') as file:
                readeractivity = csv.reader(file, delimiter = ',')
                for row in readeractivity:
                    if count_a != -1:
                        date_str2 = row[3][0:10]
                        date_obj2 = datetime.strptime(date_str2, '%Y-%m-%d')
                        
                        if plant_id == row[0] and row[2] == 'Watering' and date_obj2 > date_obj1:
                            date_obj1 = date_obj2
                    count_a = 1
                today_obj = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d')    
                if (today_obj - date_obj1).days == 1:
                    attention = 'Due Today'
                    temp_list.append([plant_id,watering_frequency,date_obj1,attention])
                    table.add_row([plant_id,watering_frequency,date_obj1,attention])   
                elif  (today_obj - date_obj1).days > 1:
                    attention = 'Past Already'
                    temp_list.append([plant_id,watering_frequency,date_obj1,attention])
                    table.add_row([plant_id,watering_frequency,date_obj1,attention])    
                         
                
                
                
        print(table)        
                    
                    
                    
            
            
    

            
    return

def seasonal_change():
    
    print("Changing seasonal details")
    print('Here is all the plants. Please choose the plant and enter its ID')
    view_all_plants()
    the_row = -1
    while True:
        try:
            plant_id = int(input('\n\nEnter the ID (Numbers) of the plant you want to log the activity:'))
        
        except:
            print('Please read through the list and enter correct ID (Numbers)')
            continue
    
        temp_list=[]
        with open('plants.csv','r') as file:
            reader = csv.reader(file, delimiter=',')
            c = 0
            for l in reader:
                if c == 0:
                    c = 1
                    continue
                temp_list.append(int(l[0]))
                c += 1
                if plant_id == int(l[0]):
                    the_row = c - 1
        if  plant_id in temp_list:
            break
        else:
            print('Please read the list and enter correct ID')
        
        
    

    rows = []

    with open("plants.csv", "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    while True:    
        try:
            new_frequency = int(input("Please enter the new frequency: "))
            if new_frequency > 0:
                break
        except:
            print("Please enter valid frequency")
        
    
    rows[the_row][4] = new_frequency

    with open("plants.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)




def add_image_path():
    
    print("Add plant image to records....")
    print('Here is all the plants. Please choose the plant and enter its ID')
    view_all_plants()
    the_row = -1
    while True:
        try:
            plant_id = int(input('\n\nEnter the ID (Numbers) of the plant you want to add an image:'))
        
        except:
            print('Please read through the list and enter correct ID (Numbers)')
            continue
    
        temp_list=[]
        with open('plants.csv','r') as file:
            reader = csv.reader(file, delimiter=',')
            c = 0
            for l in reader:
                if c == 0:
                    c = 1
                    continue
                temp_list.append(int(l[0]))
                c += 1
                if plant_id == int(l[0]):
                    the_row = c - 1
        if  plant_id in temp_list:
            break
        else:
            print('Please read the list and enter correct ID')
        
        
    

    rows = []

    with open("plants.csv", "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    while True:    
        try:
            image_path = get_non_empty("Please enter the new image path: ")
            if Path(image_path).exists():
                break
        except:
            print("Please enter valid image path")
        
    
    rows[the_row][6] = image_path

    with open("plants.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

############################################ Beginning of the program ################################################    
print('\n\n\n{{{ Welcome To Plant Tracker Program }}}\n\n\n')


main()
    