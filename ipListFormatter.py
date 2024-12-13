import re, argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

parser = argparse.ArgumentParser(
    prog="ipListFormatter",
    description="Format IP ranges from a list")
parser.add_argument("-i", "--input", help="Input file")
parser.add_argument("-o", "--output", help="Output file name (include extension)")
parser.add_argument("-n", "--name", help="Name of the IP range")
parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
parser.add_argument("-c", "--country", help="Coutry's URL to scrape.")
args = parser.parse_args()

def scrape(url, name, verbose):
    try:
        options = Options()
        options.add_argument("--headless")
        output = []
        
        driver = webdriver.Chrome(options)
        if verbose:
            print("Getting URL: " + url)
        driver.get(url)
        
        if verbose:
            print("Waiting for page to load")
        driver.implicitly_wait(15)
        
        html = driver.page_source
        driver.quit()
        
        if verbose:
            print("Parsing html")
        soup = BeautifulSoup(html, 'html.parser')
        dl = soup.find('tbody')
        for line in dl(re.compile('tr')):
            outl = re.sub(r'\<(.*?)\>', " ", str(line)).split()
            if verbose:
                print("Outl: " + str(outl))
            output.append(name+":"+outl[0] + "-" + outl[1])
        return output
    except Exception as e:
        print(e)
        exit(1)

def read(fileName, name, verbose):
    f = open(fileName, "r")
    output = []
    lines = f.readlines()
    n = 0
    for line in lines:
        if verbose:
            n += 1
            print("Line #" + str(n) + ": " + line)
        splitLine = line.split("    ")
        splitLine = splitLine[0].split("\t")
        if verbose:
            print("Split line: " + str(splitLine))
        ip1 = splitLine[0]
        ip2 = splitLine[1]
        output.append(name+":"+ip1 + "-" + ip2)
    f.close()
    return output


###
def write(fileName, ipList, verbose):
    f = open(fileName, "w")
    for ip in ipList:
        if verbose:
            print("Writing: " + ip)
        f.write(ip + "\n")
    f.close()
        
def main():    
    name = args.name
    if not name:
        name = "IP"
    out = args.output
    if not out:
        out = name+".p2p"
    url = "https://lite.ip2location.com/"+args.country+"-ip-address-ranges"
    
    if args.country:
        write(out, scrape(url, name, args.verbose), args.verbose)
    else:
        write(out, read(args.input, name, args.verbose), args.verbose)
    
if __name__ == "__main__":
    main()