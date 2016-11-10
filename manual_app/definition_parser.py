import requests
import re
from bs4 import BeautifulSoup
import csv
"""
#payload = {'key1': 'value1', 'key2': 'value2'}

#r = requests.post('http://www.zzcad.com/cgi-bin/webparse.exe', data = {'Sentence':'apply+pressure+to+wound',
#                                                                       'LinkDisplay':'on',
#                                                                      'ShortLength':'6',
#                                                                      'PageFile':'%2Fdocs%2Fsubmit-sentence-4.html&InputFile=%2Fscripts%2Finput-to-parser&Maintainer=sleator%40cs.cmu.edu'})


#s="Minor cuts and scrapes usually don't require a trip to the emergency room. These guidelines can help you care for such wounds:Wash your hands. This helps avoid infection. Also put on disposable protective gloves if they're available.Stop the bleeding. Minor cuts and scrapes usually stop bleeding on their own. If not, apply gentle pressure with a sterile bandage or clean cloth and elevate the wound.Clean the wound. Use clear water to rinse the wound. Also clean around the wound with soap and a washcloth. Keep soap out of the wound, as it can cause irritation. If dirt or debris remains in the wound after washing, use tweezers cleaned with alcohol to remove the particles. If debris still remains, see your doctor. Thorough cleaning reduces the risk of infection and tetanus. There's no need to use hydrogen peroxide, iodine or an iodine-containing cleanser, which can be irritating to tissue already injured.Apply an antibiotic. Apply a thin layer of an antibiotic cream or ointment (Neosporin, Polysporin) to help keep the surface moist. These products don't make the wound heal faster. But they can discourage infection and help the body's natural healing process. Certain ingredients in some ointments can cause a mild rash in some people. If a rash appears, stop using the ointment.Cover the wound. Bandages can help keep the wound clean and keep harmful bacteria out. If the injury is just a minor scrape, or scratch, leave it uncovered.Change the dressing. Do this at least once a day or whenever the bandage becomes wet or dirty. If the injured person is allergic to the adhesive in tapes and bandages, switch to adhesive-free dressings or sterile gauze held in place with paper tape, rolled gauze or a loosely applied elastic bandage. These supplies generally are available at pharmacies.Get stitches for deep wounds. A deep - all the way through the skin - gaping or jagged wound with exposed fat or muscle will need stitches. Adhesive strips or butterfly tape may hold a minor cut together, but if you can't easily close the wound, see your doctor as soon as possible. Proper closure within a few hours minimizes scarring and reduces the risk of infection.Watch for signs of infection. See your doctor if the wound isn't healing or you notice any redness, increasing pain, drainage, warmth or swelling.Get a tetanus shot. If the injured person hasn't had a tetanus shot in the past five years and the wound is deep or dirty, he or she may need a booster shot, as soon as possible."
s = "Apply an ointment (Vaseline, Plastibase, other) to the blister and cover it with a nonstick gauze bandage. If a rash appears, stop using the ointment."
#s = "iodine bounce blister bat"
#filterWords = csv.reader(open('filter_words.txt', 'rb'), delimiter='\n')
#filterWords = ['and','the','with','a','by','it','to','for','let','but','in','if','this','also','on','your','near','use','using','apply','more']

#Input
input = [
            ["Apply an ointment (Vaseline, Plastibase, other) to the blister and cover it with a nonstick gauze bandage. If a rash appears, stop using the ointment.","iodine bounce blister bat","Minor cuts and scrapes usually don't require a trip to the emergency room. These guidelines can help you care for such wounds:Wash your hands. This helps avoid infection."],
            ["Aim directly at the wound or infection","Place the injured arm upright or choke and burn"],
            ["Don't be dumb. Be a bandage","Take a vessel and fill it with Pills. Don't go there"]
          ]
"""

def definition_finder(input):
    results = []
    for i in range(len(input)):
        with open('filter_words.txt') as f:
            filterWords = [x.strip('\n').lower() for x in f.readlines()]
        if i==0:
            for j in range(len(input[0])):
                words = re.split('\.\s|\.|,|\s|\(|\)',input[0][j])

                res = [] 
                for word in words:
                    for filterWord in filterWords:
                        word = re.sub(r'\b%s\b' % filterWord, '', word.lower())
                    res.append(word)

                while '' in res:
                    res.remove('')



                for word in res:
                    r = requests.get('http://www.online-medical-dictionary.org/definitions-' + word[0] + '/' + word + '.html')
                    GETres = r.text
                    soup = BeautifulSoup(GETres, 'html.parser')
                    #print soup
                    uword = word[0].upper() + word[1:]
                    resQuery = '<h2>' + uword + '</h2>'
                    if resQuery in GETres:
                        try:
                            #print word + ' : ' + (soup.div.contents[2].contents[0].contents[1].contents[2].contents[0]) + (soup.div.contents[2].contents[0].contents[1].contents[2].contents[1].text)
                            temp = (soup.div.contents[2].contents[0].contents[1].contents[2].contents[0]) + (soup.div.contents[2].contents[0].contents[1].contents[2].contents[1].text)
                            templist = [word, temp, ["what is a " + word, "what's a " + word, "what is " + word, "what's " + word, "what is the definition of " + word, "what is the definition of a " + word, "what's the definition of a " + word, "what's the definition of " + word], input[0][j]]
                            results.append(templist)
                        except:
                            temp = soup.div.contents[2].contents[0].contents[1].contents[2].text
                            templist = [word, temp, ["what is a " + word, "what's a " + word, "what is " + word, "what's " + word, "what is the definition of " + word, "what is the definition of a " + word, "what's the definition of a " + word, "what's the definition of " + word], input[0][j]]
                            results.append(templist)
                        #loopCount = loopCount + 1;
                    else:
                        with open('filter_words.txt', 'a') as f:
                            f.write('\n' + word)
        else:
            for j in range(len(input[i])):
                words = re.split('\.\s|\.|,|\s|\(|\)',input[i][j])

                res = [] 
                for word in words:
                    for filterWord in filterWords:
                        word = re.sub(r'\b%s\b' % filterWord, '', word.lower())
                    res.append(word)

                while '' in res:
                    res.remove('')



                for word in res:
                    r = requests.get('http://www.online-medical-dictionary.org/definitions-' + word[0] + '/' + word + '.html')
                    GETres = r.text
                    soup = BeautifulSoup(GETres, 'html.parser')
                    #print soup
                    uword = word[0].upper() + word[1:]
                    resQuery = '<h2>' + uword + '</h2>'
                    if resQuery in GETres:
                        try:
                            #print word + ' : ' + (soup.div.contents[2].contents[0].contents[1].contents[2].contents[0]) + (soup.div.contents[2].contents[0].contents[1].contents[2].contents[1].text)
                            temp = (soup.div.contents[2].contents[0].contents[1].contents[2].contents[0]) + (soup.div.contents[2].contents[0].contents[1].contents[2].contents[1].text)
                            templist = [word, temp, ["what is a " + word, "what's a " + word, "what is " + word, "what's " + word, "what is the definition of " + word, "what is the definition of a " + word, "what's the definition of a " + word, "what's the definition of " + word], None]
                            results.append(templist)
                        except:
                            temp = soup.div.contents[2].contents[0].contents[1].contents[2].text
                            templist = [word, temp, ["what is a " + word, "what's a " + word, "what is " + word, "what's " + word, "what is the definition of " + word, "what is the definition of a " + word, "what's the definition of a " + word, "what's the definition of " + word], None]
                            results.append(templist)
                        #loopCount = loopCount + 1;
                    else:
                        with open('filter_words.txt', 'a') as f:
                            f.write('\n' + word)
        

        
            
    return results
    
    


#a = ["and","the","with","a","by","it","to","for","let","but","in","if","this","also","on","your","near","use","using","apply","more"];
#print r.text   .div.contents[2].contents[0].contents[1].contents[2]

#http://www.online-medical-dictionary.org/definitions-b/bandage.html