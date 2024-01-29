import time
def get_input():
    target_time: str=input("When should the timer go off? ")
    try:
        hours,minutes = target_time.lower().split("h")
        hours =int(hours)
        minutes = int(minutes)
        
    except:
        print("invalid format")
    else:
        return hours,minutes


#make this not freeze the whole thing while counting down (async)    
def set_timer_lenght(hours,minutes):
    current_time = time.strftime("%H:%M")
    target_time= f"{hours}:{minutes}"
    while current_time != target_time:
        time.sleep(1)
        current_time = time.strftime("%H:%M")
        print(current_time)
    print("Done")
        
def main():
    hours,minutes=get_input()
    set_timer_lenght(hours,minutes)



        
if __name__== "__main__":
    main()
