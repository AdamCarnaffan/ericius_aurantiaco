import re

class website:
    def __init__(self):
        self.body = ''' Drones claimed by Yemen's Houthi rebels attacked the world's largest oil processing facility in Saudi Arabia and a major oilfield operated by Saudi Aramco early Saturday, sparking a huge fire at a processor crucial to global energy supplies.

        It wasn't clear if there were any injuries in the attacks in Buqyaq and the Khurais oil field, nor what effect it would have on oil production in the kingdom. The attack also likely will heighten tensions further across the wider Persian Gulf amid a confrontation between the U.S. and Iran over its unravelling nuclear deal with world powers. The Houthis are backed by Tehran amid a yearslong Saudi-led war against them in Yemen.

        Online videos I apparently shot in Buqyaq included the sound of gunfire in the background. Smoke rose over the skyline and glowing flames could be seen a distance away at the Abqaiq oil processing facility.

        Saudi state television later aired a segment with a correspondent there as smoke from the blazes clearly rose behind. That smoke also was visible from space.

        The fires began after the sites were "targeted by drones," the Interior Ministry said in a statement carried by the state-run Saudi Press Agency. It said an investigation into the attack was underway.

        Rebels say attacks to worsen
        In a short address aired by the Houthi's Al-Masirah satellite news channel, military spokesperson Yahia Sarie said the rebels launched 10 drones in their co-ordinated attack on the sites. He warned attacks by the rebels would only get worse if the war continues.

        "The only option for the Saudi government is to stop attacking us," Sarie said.

        Saudi Aramco, the state-owned oil giant, did not immediately respond to questions from The Associated Press. The kingdom hopes soon to offer a sliver of the company in an initial public offering.

        Saudi Aramco describes its Abqaiq oil processing facility in Buqyaq as "the largest crude oil stabilization plant in the world."

        The facility processes sour crude oil into sweet crude, then later transports onto transshipment points on the Persian Gulf and the Red Sea. Estimates suggest it can process up to seven million barrels of crude oil a day.

        The plant has been targeted in the past by militants. Al-Qaeda-claimed suicide bombers tried but failed to attack the oil complex in February 2006.

        No immediate impact on oil prices
        The Khurais oil field is believed to produce over a million barrels of crude oil a day. It has estimated reserves of over 20 billion barrels of oil, according to Aramco.

        There was no immediate impact on global oil prices as markets were closed for the weekend across the world. Benchmark Brent crude had been trading at just above $60 US a barrel.

        Buqyaq is some '330 kilometres northeast of the Saudi capital, Riyadh.' 

        The Saudi-led coalition has been battling the rebels since March 2015. The Iranian-backed Houthis hold Yemen's capital, Sanaa, and other territory in the Arab world's poorest country.

        World's worst humanitarian crisis
        The war has become the world's worst humanitarian crisis. The violence has pushed Yemen to the brink of famine and killed more than 90,000 people since 2015, according to the U.S.-based Armed Conflict Location & Event Data Project, or ACLED, which tracks the conflict.

        Since 'the start of the Saudi-led war, 'Houthi rebels have been using drones in' combat. The first appeared to be off-the-shelf, hobby-kit-style drones.' Later, versions nearly identical to Iranian models turned up. Iran denies supplying the Houthis with weapons, although the UN, the West and Gulf Arab nations say Tehran does.

        The rebels have flown drones into the radar arrays of Saudi Arabia's Patriot missile batteries, according to Conflict Armament Research, disabling them and allowing the Houthis to fire ballistic missiles into the kingdom unchallenged. The Houthis launched drone attacks targeting Saudi Arabia's crucial East-West Pipeline in May as tensions heightened between Iran and the U.S. In August, Houthi drones struck Saudi Arabia's Shaybah oil field, which produces some 1 million barrels of crude oil a day near its border with the United Arab Emirates.

        UN investigators said the Houthis' new UAV-X drone, found in recent months during the Saudi-led coalition's war in Yemen, likely has a range of up to 1,500 kilometres.

        That puts the far reaches of both Saudi Arabia and the UAE in range. '''

    def getQuotes(self, isQuote):
        # count sections of body between quotation marks
        c1 = 0
        quotes = []
        notQuotes = []
        for partition in self.body.rjust(1).split('"'):
            c1 += 1
            if c1 % 2 == 0:
                # confirm quote is longer than 5 words
                if len(partition.split()) > 5:
                    quotes.append(partition)
            else:
                notQuotes.append(partition)

        if (isQuote):
            return quotes
        else:
            return notQuotes

        
    # determine number of citations in page
    def citations(self):
        citations = len(self.getQuotes(True))
        return citations

    # COMBAK: we need to define fluff
    def fluff(self):
        fluff = 0
        return fluff

    def opinion(self):
        # count first person pronouns not in quotes
        text = self.getQuotes(False)
        pronouns = 0
        for words in text:
            pronouns += len(re.findall(r'(\Wi\W|\Wme\W|\Wwe\W|\Wus\W|\Wmyself\W|\Wmy\W|\Wour\W|\Wours\W)', words.lower()))
        return pronouns


site = website()
print(site.opinion())
