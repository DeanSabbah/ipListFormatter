import re, argparse, traceback
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

verbose:bool = args.verbose

def scrape(country:str, name:str) -> list[str]:
    try:
        url = f"https://lite.ip2location.com/{country.lower()}-ip-address-ranges"
        options = Options()
        options.add_argument("--headless")
        output = []
        
        driver = webdriver.Chrome(options)
        if verbose:
            print("Getting URL: " + url)
            print("Waiting for page to load")
        driver.get(url)
        
        html = driver.page_source
        driver.quit()
        
        if verbose:
            print("Parsing html")
        soup = BeautifulSoup(html, 'html.parser')
        dl = soup.find('tbody')
        count = 0
        for line in dl(re.compile('tr')):
            outl = re.sub(r'\<(.*?)\>', " ", str(line)).split()
            if "Loading" in outl[0]:
                print("Error getting page. Try again later.")
                exit(1)
            if verbose:
                print("Outl: " + str(outl))
            try:
                count += int(outl[2].replace(",", ""))
            except:
                if verbose:
                    print("Not a number")
                pass
            output.append(name+":"+outl[0] + "-" + outl[1])
        if verbose:
            print("Total IPs: " + str(count))
        output.append("# Total IPs: " + str(count))
        return output
    except Exception:
        print(traceback.format_exc())
        exit(1)

def read(fileName:str, name:str) -> list[str]:
    try:
        f = open(fileName, "r")
        output = []
        lines = f.readlines()
        n = 0
        count = 0
        for line in lines:
            if verbose:
                n += 1
                print("Line #" + str(n) + ": " + line)
            splitLine = line.split()
            if verbose:
                print("Split line: " + str(splitLine))
            try:
                count += int(splitLine[2].replace(",", ""))
            except:
                if verbose:
                    print("Not a number")
                pass
            output.append(name+":"+splitLine[0] + "-" + splitLine[1])
        if verbose:
            print("Total IPs: " + str(count))
        output.append("# Total IPs: " + str(count))
        f.close()
        return output
    except Exception:
        print(traceback.format_exc())
        exit(1)


def write(fileName:str, ipList:list[str]) -> None:
    try:
        f = open(fileName, "w")
        f.write("#"*86+"\n")
        if args.country:
            f.write("#"f"{f'List scraped from https://lite.ip2location.com/{args.country.lower()}-ip-address-ranges':^84}""#\n")
        f.write(f"#"f"{'Scraper/Formatter by Dean Sabbah':^84}""#\n")
        f.write("#"f"{'https://github.com/DeanSabbah/ipListFormatter':^84}""#\n")
        f.write("#"*86+"\n")
        for ip in ipList:
            if verbose:
                print("Writing: " + ip)
            f.write(ip + "\n")
        f.close()
    except Exception:
        print(traceback.format_exc())
        exit(1)
        
def main():
    if not args.country and not args.input:
        print("Please provide an input file or a country name to scrape.")
        exit(1)
    name:str = args.name
    if not name:
        name = "IP"
    out:str = args.output
    if not out:
        out = name+".p2p"
    
    # I don't really need to pass the arguments in the function call but it
    # makes it easier to handle optinal arguments.
    if args.country:
        write(out, scrape(args.country, name))
    else:
        write(out, read(args.input, name))
    
if __name__ == "__main__":
    main()