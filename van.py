import csv, random, math
class Van:
    def __init__(self, num, riders=[]):
        self.num = num
        for rider in riders:
            if rider.isCoxswain():
                self.coxswains += 1
        if riders==[]:
            self. riders = []
    def __str__(self):
        string = f"Van {self.num}: "
        for rider in self.riders:
            if rider.fname:
                string += f"{rider.fname[0]}. {rider.lname} | "
            else:
                string += f"{rider.lname} | "
        #string += f"\tRiders: {self.numriders()}"
        return string
    def getCoxswains(self):
        coxswains = 0
        for rider in self.riders:
            if rider.cox:
                coxswains += 1
        return coxswains
    def getNovii(self):
        novii = 0
        for rider in self.riders:
            if rider.nov:
                novii += 1
        return novii
    def getDrivers(self):
        drivers = 0
        for rider in self.riders:
            if rider.driver:
                drivers += 1
        return drivers
    def getBoard(self):
        board = 0
        for rider in self.riders:
            if rider.bmem:
                board += 1
        return board
    def addRider(self, rider):
        self.riders += [rider]
    def numriders(self):
        return len(self.riders)
class Rider:
    def __init__(self, fname, lname, driver, cox, nov, bmem, boat):
        self.fname = fname
        if len(fname) == 0:
            self.fname = " "
        self.lname = lname
        self.driver = driver
        self.cox = cox
        self.nov = nov
        self.bmem = bmem
        self.boat = boat
        self.van = None
    def __str__(self):
        return f"{self.fname} {self.lname}"
    def isCoxswain(self):
        return self.cox 
    def setVan(self, van):
        self.van = van
    def setVan(self, van):
        self.van = van
    def hasVan(self):
        if self.van:
            return True
def minpass(vans):
    minlen = vans[0].numriders()
    minlenvan = vans[0].num
    for i in range(0, len(vans)):
        if vans[i].numriders() < minlen:
            minlen = vans[i].numriders()
            minlenvan = vans[i].num
    return minlen
def mindriver(vans):
    mindriver = vans[0].getDrivers()
    mindrivervan = vans[0].num
    for i in range(0, len(vans)):
        if vans[i].getDrivers() < mindriver:
            mindriver = vans[i].getDrivers()
            mindrivervan = vans[i].num
    return mindriver
CSV_PATH = r"C:\\Users\sawye\Downloads\drivers.csv"
riders = []
with open(CSV_PATH) as csvfile:
    for row in csv.reader(csvfile):
        if row[0] == "First Name":
            continue
        # First name, last name, driver, coxswain, novice, board, boat
        riders += [Rider(row[0], row[1], row[2][0].lower()=="y", row[3][0].lower()=="y", row[4][0].lower()=="y", row[5][0].lower()=="y", row[6])]
random.shuffle(riders)
loop = -1
maxriders = 6
numvans = math.ceil(len(riders) / maxriders)
curvan = 0
vans = []
for i in range(numvans):
    vans += [Van(i)]
board = []
drivers = []
coxswains = []
novii = []
for rider in riders:
        if rider.bmem:
            board += [rider]
        if rider.cox:
            coxswains += [rider]
        if rider.driver:
            drivers += [rider]
        if rider.nov:
            novii += [rider]
for bmem in board:
    minriders = minpass(vans)
    if not bmem.hasVan():
        added = False
        for inc in range(0, maxriders):
            for van in vans: 
                if van.getBoard() == 0 and van.numriders() == minriders + inc and van.numriders() < maxriders:
                    bmem.setVan(van)
                    van.addRider(bmem)
                    added = True
                    break
            break
        if not added:
            for van in vans:
                if van.numriders() < maxriders:
                    bmem.setVan(van)
                    van.addRider(bmem)
                    added = True
                    break
for driver in drivers:
    minriders = minpass(vans)
    mindrivers = mindriver(vans)
    if not driver.hasVan():
        for van in vans:
            if van.numriders() == minriders and van.getDrivers() < 2:
                driver.setVan(van)
                van.addRider(driver)
                break
maxcoxvans = math.ceil(len(coxswains) / 2.5)
for cox in coxswains:
    if cox.hasVan():
        continue
    minvan = minpass(vans)
    coxvans = 0
    for van in vans:
        if van.getCoxswains() > 0:
            coxvans += 1
    while coxvans < maxcoxvans:
        if cox.hasVan():
            break
        for van in vans:
            if van.getCoxswains() == 0:
                cox.setVan(van)
                van.addRider(cox)
                coxvans += 1
                break
    if cox.hasVan():
        continue
    for van in vans:
        if van.getCoxswains() == 1:
            cox.setVan(van)
            van.addRider(cox)
            break
for cox in coxswains:
    if cox.hasVan():
        continue
    for van in vans:
        if van.getCoxswains() == 2 and van.numriders() < maxriders:
            van.addRider(cox)
            cox.setVan(van)
            break
novcoxes = []
for rider in riders:
    if rider.nov and rider.cox:
        novcoxes += [rider]
for novcox in novcoxes:
    van = novcox.van
    for nov in novii:
        if nov.hasVan():
            continue
        if van.getNovii() < 2 and van.numriders() < maxriders and van.numriders() < maxriders:
            van.addRider(nov)
            nov.setVan(van)
        break
for nov in novii:
    if nov.hasVan():
        continue
    for van in vans:
        if van.getNovii() < 2:
            if van.getCoxswains() > 0 and van.numriders() < maxriders:
                continue
            van.addRider(nov)
            nov.setVan(van)
            break
for driver in drivers:
    if driver.hasVan():
        continue
    for van in vans:
        if van.getDrivers() < 3 and van.numriders() < maxriders:
            van.addRider(driver)
            driver.setVan(van)
            break
for rider in riders:
    minriders = minpass(vans)
    if rider.hasVan():
        continue
    for van in vans:
        if van.numriders() == minriders and van.numriders() < maxriders:
            van.addRider(rider)
            rider.setVan(van)
            break
for van in vans:
    print(van)
for van in vans:
    # Coxswain check
    coxswains = van.getCoxswains()
    if coxswains == 1:
        print(f"Warning: Van {van.num} has a lone coxswain.")
        break
    elif coxswains > 3:
        print(f"Warning: Van {van.num} has more than three coxswains.")
        break
    
    # Novice check
    novii = van.getNovii()
    if novii == 0:
        print(f"Warning: Van {van.num} has no novices.")
        break
    elif novii == 1:
        print(f"Warning: Van {van.num} has a lone novice.")
        break

    # Driver check
    drivers = van.getDrivers()
    if drivers < 2:
        print(f"Warning: Van {van.num} has fewer than three drivers.")
        break
inpt = input("Save van assignments? (y/n) ")
if inpt:
    with open('output.csv', 'w', newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Truck", "S. Armstrong", "M. Hyndman"])
        for van in vans:
            lst = [f"Van {van.num}"]
            for rider in van.riders:
                lst = lst + [f"{rider.fname[0]} {rider.lname}"]
            csvwriter.writerow(lst)