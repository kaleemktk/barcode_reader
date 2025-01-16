import evdev, struct, time, sys, os, re, time
from evdev import InputDevice, categorize, ecodes

print("Running: "+os.getcwd()+"/"+sys.argv[0])
i=0
found_flag=0
print("Searching for any BarCode Scanner connected ? ......")
model_file=open('models.txt','r')
model_lines=model_file.read().splitlines()
dev_file=open('/proc/bus/input/devices', 'r')
dev_lines=dev_file.readlines()

for line in dev_lines:
    if found_flag!=1:
        for l in model_lines:
            l=l.strip()
            if l in line:
                print("Scanner Found"+" as device : "+ line)
                print("Searching for Bar Code Scanner Event Number....")
                found_flag=1
                break
    if found_flag==1:
        if re.search("event",line):
            event_num=line.split()[-1]
            print("Event Number was found for bar code scanner as : "+event_num)
            break
    i=i+1
        
if found_flag==0:
    print("Scanner NOT Attached\nPlease Attach Scanner to USB port and try again!\n",file=sys.stderr)
    exit(2)


result_str=""
kb_dev=evdev.InputDevice('/dev/input/'+event_num)

for event in kb_dev.read_loop():
    if event.type ==ecodes.EV_KEY:
        key_pressed=str(categorize(event))
        if 'down' in key_pressed:
            fields=key_pressed.split()[5]
            key_found=re.sub("\(KEY_","",fields)
            key_found=re.sub("\),","",key_found)
            result_str=result_str+key_found
            if re.search("^[0-9]{7}$", result_str): 
                print("Correct Work Order Number Found:",result_str)
                print("Exiting\n")
                sys.exit(0)

            if len(result_str) > 6:
                print('Error: Incorrect Work Order Number Format',file=sys.stderr)
                sys.exit(1)




