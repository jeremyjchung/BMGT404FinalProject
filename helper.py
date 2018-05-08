def secondsToTime(t):
    h = int(t / 3600)
    m = int((t - h * 3600) / 60)
    s = int(t - h * 3600 - m * 60)

    return "%02d:%02d:%02d" % (h, m, s)

def foodToStr(lst):
    return "\n".join(list(map(lambda x: str(x[0]) + "\t\t" + str(x[1]), lst)))

def calculateOrderTime(food):
    #initial_wait_time = int(priority_order[2])*15 + int(priority_order[3])*10 + int(priority_order[4])*10 + \
        #int(priority_order[5])*10 + int(priority_order[6])*15 + \
        #int(priority_order[7])*10 + int(priority_order[8])*5
        #menu = ['Calzone','Salad','Tots','Stix','Wings','Dessert','Drink']
    time = 0
    for (item, quantity) in food:
        if item == 'Calzone':
            time += 780 + 120*quantity
        elif item == 'Salad':
            time += 420 + 180*quantity
        elif item == 'Tots':
            time += 360 + 120*quantity
        elif item == 'Stix':
            time += 480 
        elif item == 'Wings':
            time += 420 + 240*quantity
        elif item == 'Dessert':
            time += 600 + 180*quantity
        elif item == 'Drink':
            time += 60 + 30*quantity
    return time