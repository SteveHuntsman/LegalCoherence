#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 21:27:55 2024

@author: sha0639
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%
import os
os.environ['OPENAI_API_KEY'] = '0'# insert yours here

#%%
from openai import OpenAI
client = OpenAI()

#%%
import re
leadingNumber = re.compile(r"^\d*\. ")  # for removing leading strings like '2. ', etc.

#%%
import numpy as np

#%%
import pickle

#%% Lightly edited extract from the formal report
context = "I.    PRELIMINARY STATEMENT\n 1.    By order of General George B. Crist, USMC, Commander in Chief, U.S. Central Command, dated 3 July 1988, Rear Admiral William M. Fogarty, USN, Director, Policy and Plans (J-5), U.S. Central Command, was appointed to conduct a formal investigation into the circumstances surrounding the downing of a commercial airliner by the USS VINCENNES on 3 July 1988.\n …\n 11.    During the investigation, the importance of the information being presented by way of the USS VINCENNES Large Screen Displays (LSD) became apparent. Therefore, an explanation of that system's capabilities and limitations is provided here for the benefit of the reviewer. \n The AEGIS Large Screen Display (LSD) is a part of the AEGIS Display System (ADS) and is a primary visual information source for the CO, TAO and Force Warfare Commanders. It consists of four 42 inch x 42 inch flat, vertically mounted, 2-dimensional displays which display the tactical picture contained in the C&D computers. This information is displayed as Navy Tactical Display System (NTDS) symbology with appropriate velocity leaders. The range scales can be varied from [redacted] nautical miles. Geographic outline maps as well as operator selectable line segments, points, circles and ellipses can also be displayed. These latter items can be used to construct operational areas, geographic features, range rings, air lanes, etc. The display operator can also attach a 24 character alphanumeric label (or 'tag') to any track or point. Therefore, the track classification, ID, position relative other tracks, range, bearing, course and speeds as well as position relative to geographic features or air lanes, etc., can be displayed. However, it is important to note, that altitude cannot be displayed on the LSD in real-time.\n …\n II.    EXECUTIVE SUMMARY\n A.    INTRODUCTION\n 1.    3 July 1988, the USS VINCENNES (CG 49), operating in the Southern Persian Gulf as a unit assigned to Commander, Joint Task Force Middle East, downed a civilian airliner, Iran Air Flight 655 on a routine scheduled flight from Bandar Abbas to Dubai, with two SM-2 missiles.\n 2.    The material condition, combat systems, training and personnel readiness of the ship were satisfactory. \n 3.    The following narrative summarizes the events leading up to and including the downing of Iran Air Flight 655. It is in the form of a chronology because the situation leading up to, just prior to, and during the few critical minutes from Iran Air Flight 655 takeoff to downing are considered important to a full understanding of the incident. All times in the report are 'Z' time.\n B.    PRE-3 JULY SCENARIO\n 1.    In the three day period prior to the incident, there was heightened air and naval activity in the Persian Gulf. Iraq conducted air strikes against Iranian oil facilities and shipping 30 June through 2 July 1988. Iranian response was to step up ship attacks. Additionally, Iran deployed F-14's from Bushehr to Bandar Abbas. U.S. Forces in the Persian Gulf were alerted to the probability of significant Iranian military activity resulting from Iranian retaliation for recent Iraqi military successes. That period covered the fourth of July holiday weekend.\n 2.    During the afternoon and evening hours of 2 July 1988 and continuing into the morning of 3 July 1988, Iranian Revolutionary Guard Corps (IRGC) armed small boats (Boghammers, and Boston Whalers) positioned themselves at the western approach to the Strait of Hormuz (SOH). From this position, they were challenging merchant vessels, which has been a precursor to merchant ship attacks. On 2 July 1988, USS ELMER MONTGOMERY was located sufficiently close to a ship attack in progress as to respond to a request for distress assistance and to fire warning shots to ward off IRGC small boats attacking a merchant vessel.\n C.    3 JULY SURFACE ENGAGEMENT\n 1.    On the morning of 3 July 1988, USS ELMER MONTGOMERY was on patrol in the northern portion of the Strait of Hormuz. At approximately 0330Z, USS MONTGOMERY observed seven small Iranian gunboats approaching a Pakistani merchant vessel. The small boats were reported by USS MONTGOMERY to have manned machine gun mounts and rocket launchers. \n Shortly thereafter, USS MONTGOMERY observed a total of 13 Iranian gun boats breaking up into three groups. Each group contained 3 to 4 gun boats with one group of four gun boats taking position off USS MONTGOMERY's port quarter. At 0411Z, USS MONTGOMERY heard the gun boats over bridge to bridge challenging merchant ships in the area. USS MONTGOMERY then heard 5 to 7 explosions coming from the north. At 0412Z, 'Golf Sierra' directed USS VINCENNES to proceed north to the vicinity of USS MONTGOMERY and investigate USS MONTGOMERY's report of small boats preparing to attack a merchant ship. USS VINCENNES's helo (OCEAN LORD 25/Lamps MK-III helo) on routine morning patrol, was vectored north to observe the Iranian small boat activity. USS VINCENNES was also monitoring a routine maritime patrol of an Iranian P-3 operating to the west. At approximately 0615Z, the USS VINCENNES's helicopter was fired upon by one of the small boats. USS VINCENNES then took tactical command of USS MONTGOMERY and both ships proceeded to close the position of the helicopter and the small boats at high speed. As USS VINCENNES and USS MONTGOMERY approached the position of the small boats, two of them were observed to turn towards USS VINCENNES and USS MONTGOMERY. The closing action was interpreted as a demonstration of hostile intent. USS VINCENNES then requested and was given permission by CJTFME to engage the small boats with gunfire. At approximately 0643Z, USS VINCENNES opened fire and was actively involved in the surface engagement from the time Iranian Air Flight 655 took off from Bandar Abbas through the downing of Iran Air Flight 655.\n 2.    During the course of the gun engagement of the Iranian small boats, the USS VINCENNES, at approximately O654Z, had maneuvered into a position one mile west of the centerline of civilian airway Amber 59. The USS SIDES, transiting from east to west through the SOH, was approximately 18 miles to the east and became involved in the evolving tactical situation."

#%% Lightly edited from III.C.1.b of the formal report
# "CAPT Rogers recalled having the following indicators in declaring track 4131 hostile and deciding to engage"
positiveEvidence = ["F-14s had been recently moved to Bandar Abbas.",
    "Iranian fighters had flown coincident with surface engagement on 18 April 1988.",
    "Track 4131 was not responding to verbal warnings over [air distress frequencies].",
    "There had been warnings of an increased threat over the July 4th weekend.",
    "Increased hostile activity had been predicted for the 48 hours following recent Iraqi military victory.",
    "Track 4131 was not following the air corridor in the same manner as other commercial aircraft had been seen consistently to behave (i.e. flying exactly on the centerline).",
    "Track 4131 was flying at a reported altitude which was lower than [commerical airliners] were observed to fly in the past.",
    "Track 4131 was reported to be increasing in speed.",
    "Track 4131 was reported to be decreasing in altitude.",
    "Track 4131 was [at constant bearing, with decreasing range] to USS VINCENNES and USS MONTGOMERY.",
    "Track 4131 was reported by USS VINCENNES's personnel squawking Mode II-1100 which correlates with an F-14.",
    "No [electronic emissions were reported] from track 4131, however, F-14s can fly [without electronic emissions].",
    "F-14s have an air-to-surface capability with Maverick and modified Eagle missiles.",
    "Track 4131 appeared to be maneuvering into an attack position.",
    "Visual identification of track 4131 was not feasible."]

#%%
negativeEvidenceIndices = [5,6,8]
# Negation of [positiveEvidence[i] for i in negativeEvidenceIndices]
negativeEvidence = ["Track 4131 was following the air corridor in the same manner as other commercial aircraft had been seen consistently to behave (i.e. flying exactly on the centerline).",
    "Track 4131 was flying at a reported altitude which was the same as commerical airliners were observed to fly in the past.",
    "Track 4131 was reported to be increasing in altitude."]

#%%
evidence = positiveEvidence+negativeEvidence

#%%
hypotheses = positiveHypotheses+negativeHypotheses

#%% 
positiveHypotheses = ["Iran was intending to mount an attack.",
                      "Track 4131 was an F-14.",
                      "Track 4131 intended to attack.",
                      "Track 4131 was flying without electronic emissions."]

#%%
negativeHypotheses = ["Track 4131 was a commercial airliner.",
                      "Track 4131 was taking off."]

#%% Special treatment to avoid pointless effort
claimPairsEvi = [[positiveEvidence[negativeEvidenceIndices[i]],negativeEvidence[i]] for i in range(len(negativeEvidenceIndices))]

#%%
claimPairsEviHyp = []
for i1 in range(len(evidence)):
    for i2 in range(len(hypotheses)):
        claimPairsEviHyp.append([evidence[i1],hypotheses[i2]])

#%%
claimPairsPosHypPosHyp = []
for i1 in range(len(positiveHypotheses)):
    for i2 in range(i1+1,len(positiveHypotheses)):
        claimPairsPosHypPosHyp.append([positiveHypotheses[i1],positiveHypotheses[i2]])
#
claimPairsPosHypNegHyp = []
for i1 in range(len(positiveHypotheses)):
    for i2 in range(len(negativeHypotheses)):
        claimPairsPosHypNegHyp.append([positiveHypotheses[i1],negativeHypotheses[i2]])
#
claimPairsNegHypNegHyp = []
for i1 in range(len(negativeHypotheses)):
    for i2 in range(i1+1,len(negativeHypotheses)):
        claimPairsNegHypNegHyp.append([negativeHypotheses[i1],negativeHypotheses[i2]])
#
claimPairsHyp = claimPairsPosHypPosHyp+claimPairsPosHypNegHyp+claimPairsNegHypNegHyp

#%%
claimPairs = claimPairsEvi+claimPairsEviHyp+claimPairsHyp

#%%
consistencyInit = 'Imagine you are a perfectly objective arbitrator with impeccable judgment and integrity. In response to a prompt of the form "evalConsistency: " followed by two claims in braces that are separated by a space, please do two things. First, explain the logical relationship between the two claims, assuming that the first claim is true, whether or not it actually is. I want you to ignore the truth, falsity or basis in fact of either claim. Second, use your explanation to numerically rate the relative consistency of the two claims. Do not pay attention to or comment on the truth or basis in fact of either claim independent of the other. Your rating of relative consistency should be on a scale from 0 to 10, with a value of 0 for a pair of claims that are not at all consistent and a value of 10 for a pair of claims that are totally consistent. I cannot emphasize enough that for your rating, I want you to ignore the truth or basis in fact of either claim, since anything that is not consistent with reality cannot be true. To be clear, a pair of unrelated claims should be rated a 10 and a pair of false but consistent claims should also be rated a 10. Meanwhile, a pair of claims of which one is true and the other is false, should be rated a 0. Your numerical rating should be delimited by "#" characters on both sides. \n\n For example, the prompt \n\n "evalConsistency: {The earth is flat} {The sky is red}" \n\n should produce a response like \n\n "The shape of the earth and color of the sky are unrelated, so the consistency rating of these claims is #10#." \n\n As another example, the prompt \n\n "evalConsistency: {Purple people are evil} {Purple people are good}" \n\n should produce a response like \n\n "If either claim is true, then the other is false, so the consistency rating of these claims is #0#."' 

#%%
establish = "I want to establish context for our conversation using the following passage delimited by braces, before giving you a task below.\n\n{"
preamble = (establish
            +context
            +"}\n\nWith that context established:\n\n"
            +consistencyInit
            +"\n\nevalConsistency: {")

#%%
propositions = negativeHypotheses+negativeEvidence+evidence+positiveHypotheses

#%%
relevanceInit = 'Imagine you are a perfectly objective arbitrator with impeccable judgment and integrity. In response to a prompt of the form "mostRelevant: " followed by a list of claims in braces that are separated by spaces, explain which three or fewer claims in the list have the strongest logical relationship (i.e., the most relevance) to the very first claim in the list. Towards this end, I want you to ignore the truth, falsity or basis in fact of any of the claims, and to focus on their relationships. Therefore, do not include any claims that do not have a strong logical relationship with the first claim. Also, quote the claims exactly. For example, if presented with "mostRelevant: {[z]} {[a]} {[b]} {[c]} {[d]} {[e]}" where [z], [a],... [e] indicate claims, and where [d], [a], and [c] have the strongest logical relationships with [z], then any answer you return should finish with "{[d]} {[a]} {[c]}.'

#%%
preambleRelevance = establish+context+"}\n\nWith that context established:\n\n"+relevanceInit+"\n\nmostRelevant: "

#%%
mostRelevant = []
for p in range(len(propositions)):
    # str puts propositions[p] first, then the rest in order, all in braces
    complement = list(set(range(len(propositions))).difference(set([p])))
    str = " {"+propositions[p]
    for q in range(len(complement)):
        str = str+"} {"+propositions[complement[q]]
    str = str+"}"
    relevancePrompt = preambleRelevance+str
    #
    completion3 = client.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        messages = [
            {"role": "system", "content": relevanceInit},
            {"role": "user", "content": relevancePrompt}
        ]
    )


#%%
N = 10;
# Initializations
details3 = []
details4 = []
scores3 = np.zeros([len(claimPairs),N])
scores4 = np.zeros([len(claimPairs),N])
# Loop
for j in range(len(claimPairs)):
    str1 = claimPairs[j][0]
    str2 = claimPairs[j][1]
    details3_j = []
    details4_j = []
    consistencyPrompt = preamble+str1+"} {"+str2+"}"
    # Loop over realizations
    for k in range(N):
        print(str(j+1)+"/"+str(len(claimPairs))+"; "+str(k+1)+"/"+str(N))
        #%% Interact with ChatGPT following this example:
        #        
        # completion = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        #         {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        #   ]
        # )
        #
        # print(completion.choices[0].message)
        #
        #%%
        # Models from https://platform.openai.com/docs/models
        #%%
        completion3 = client.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            messages = [
                {"role": "system", "content": consistencyInit},
                {"role": "user", "content": consistencyPrompt}
            ]
        )
        completion4 = client.chat.completions.create(
            model = "gpt-4-turbo-2024-04-09",
            messages = [
                {"role": "system", "content": consistencyInit},
                {"role": "user", "content": consistencyPrompt}
            ]
        )
        # Extract response from ChatGPT
        foo3 = completion3.choices[0].message.content
        foo4 = completion4.choices[0].message.content
        # Extract the numerical rating (or NaN if none is to be found)
        try:
            tmp = re.findall(r'#.+#',foo3)[-1]
            bar3 = float(tmp.strip('#'))
        except Exception: 
            foo3 = ''
            bar3 = float("NaN")
        try:
            tmp = re.findall(r'#.+#',foo4)[-1]
            bar4 = float(tmp.strip('#'))
        except Exception: 
            foo4 = ''
            bar4 = float("NaN")
        # Append results
        scores3[j,k] = bar3
        scores4[j,k] = bar4
        details3_j.append(foo3)
        details4_j.append(foo4)
    # Append results
    details3.append(details3_j)
    details4.append(details4_j) # bug fixed from earlier version
    # Pickle/save
    with open('consistencyDataVincennes.pkl','wb') as f:
        # pickle.dump([details3,scores3],f)
        pickle.dump([details3,details4,scores3,scores4],f)

#%% https://stackoverflow.com/a/47626762
import json
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

#%% Extra saves
with open('claimPairs.json', 'w', encoding='utf-8') as f:
    json.dump(claimPairs, f, ensure_ascii=False, indent=4)
with open('details3Vincennes.json', 'w', encoding='utf-8') as f:
    json.dump(details3, f, ensure_ascii=False, indent=4)
with open('details4Vincennes.json', 'w', encoding='utf-8') as f:
    json.dump(details4, f, ensure_ascii=False, indent=4)
# json_dump = json.dumps({'details3': details3,'scores3': scores3},cls=NumpyEncoder)
json_dump = json.dumps({'details3': details3, 'details4': details4,
                        'scores3': scores3, 'scores4': scores4}, 
                        cls=NumpyEncoder)
with open('consistencyDataVincennes.json', 'w', encoding='utf-8') as f:
    json.dump(json_dump, f, ensure_ascii=False, indent=4)
