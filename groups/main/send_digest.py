#!/usr/bin/env python3
import json
import base64
import urllib.request
import urllib.parse

# Load credentials
with open('/home/node/.gmail-mcp/credentials.json') as f:
    creds = json.load(f)

with open('/home/node/.gmail-mcp/gcp-oauth.keys.json') as f:
    keys = json.load(f)['installed']

# Refresh access token
token_data = urllib.parse.urlencode({
    'client_id': keys['client_id'],
    'client_secret': keys['client_secret'],
    'refresh_token': creds['refresh_token'],
    'grant_type': 'refresh_token',
}).encode()

req = urllib.request.Request(
    'https://oauth2.googleapis.com/token',
    data=token_data,
    method='POST',
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)
with urllib.request.urlopen(req) as resp:
    token_resp = json.load(resp)

access_token = token_resp['access_token']
print(f"Token refreshed successfully.")

# Email content
email_body = """Subject: Space & Atoms -- 2026-05-09 Weekly
From: enzolodi42@gmail.com
To: giovanni.lodi42@gmail.com
Content-Type: text/plain; charset=utf-8
MIME-Version: 1.0

Space & Atoms -- 2026-05-09 Weekly
Week of May 2-9, 2026
======================


PLANET LABS
-----------
Three new Pelican satellites (including one dedicated to the Swedish Armed Forces) launched May 3 on a SpaceX rideshare from Vandenberg. Each carries an NVIDIA Jetson AI platform for on-orbit edge compute. This follows the April 7 milestone where Pelican-4 ran AI object detection onboard -- 500 km over Alice Springs, it imaged an airport and detected aircraft using an NVIDIA Jetson Orin module, running inside isolated Docker containers with 80% detection accuracy. Planet plans to run the full inference pipeline (capture, detection, geo-rectification) in orbit. Gen 2 Pelicans targeting 30 cm resolution are due later in 2026.

Launch announcement (May 3):
https://spacewatch.global/2026/05/planet-launches-three-high-resolution-pelican-satellites-including-one-for-the-swedish-armed-forces/

Pelican-4 AI details (April 7):
https://www.satellitetoday.com/imagery-and-sensing/2026/04/07/planet-details-ai-driven-object-detection-onboard-pelican-4-satellite/

Planet Labs notebooks repo added SuperRes example notebook (May 4-5):
https://github.com/planetlabs/notebooks/commit/0f757fcd0f1d5ff780d0aa1e4f140cd4695e6ea5


NASA
----
Artemis II post-mission engineering analysis published May 4. Key data: Orion traveled 694,481 miles, entered atmosphere at 35x the speed of sound, touched down 2.9 miles from target (within 1 mph of predictions). The heat shield charring seen on Artemis I was significantly reduced. SLS achieved insertion point with high precision, launch pad sustained minimal damage. Engineers are now examining a urine vent line anomaly before Artemis III (targeted 2027).

https://sciencedaily.com/releases/2026/05/260504023837.htm

F Prime (flight software framework) active issues this week -- two security-relevant bugs filed May 8: a missing bounds check before memcpy in TlmPacketizer's TlmRecv_handler (potential buffer overflow) and an invalid-input case in SET_LEVEL_cmdHandler returning OK instead of error. Latest release v4.2.2 shipped April 24.

Buffer overflow issue: https://github.com/nasa/fprime/issues/5118
SET_LEVEL bug: https://github.com/nasa/fprime/issues/5119
v4.2.2 release: https://github.com/nasa/fprime/releases/tag/v4.2.2

Space ROS shipped jazzy-2026.04.0 on May 1, the quarterly release based on ROS 2 Jazzy Jalisco:
https://github.com/space-ros/space-ros/releases/tag/jazzy-2026.04.0


BLUE ORIGIN
-----------
New Glenn remains grounded after the April 19 NG-3 mission placed AST SpaceMobile's Bluebird 7 in the wrong orbit. CEO Dave Limp confirmed the root cause: a thrust anomaly during the second upper stage burn where one BE-3U engine failed to produce sufficient thrust. The FAA is overseeing the investigation; Blue Origin must identify the root cause, design a fix, and get FAA approval before return to flight. No timeline given.

FAA grounds New Glenn (April 21):
https://www.theregister.com/2026/04/21/faa_wants_a_closer_look/

Blue Origin's technical explanation (April 23):
https://gizmodo.com/blue-origin-offers-an-explanation-for-its-embarrassing-satellite-mishap-2000750010


X-ENERGY (Xe-100)
-----------------
Curtiss-Wright announced May 6 it has transitioned from design to prototype manufacturing of two critical Xe-100 systems: the Helium Circulator (circulates helium through the primary loop to transfer thermal energy from core to steam generator) and the Reactivity Control and Shutdown Systems. The Xe-100 is a Gen IV high-temperature gas-cooled reactor delivering 80 MWe per unit (320 MWe per four-unit plant). This is a meaningful step from paper to physical hardware.

https://www.businesswire.com/news/home/20260506692971/en/Curtiss-Wright-Announces-Transition-From-Design-to-Prototype-Manufacturing-of-Helium-Circulator-and-Safety-Systems-for-X-energys-Xe-100-Reactor


THE NUCLEAR COMPANY
-------------------
May 4: Brookfield Asset Management and The Nuclear Company announced a partnership to form a new company focused on deploying Westinghouse AP1000 and AP300 reactors. The new entity combines TNC's Nuclear Operating System (NOS, an AI-driven platform for data-driven construction management) with Brookfield's infrastructure capital. Their stated approach: design-once, build-many, with end-to-end EPC and licensing support.

https://www.thenuclearcompany.com/posts/brookfield-and-the-nuclear-company-form-new-company


ANSTO (AUSTRALIAN NUCLEAR SCIENCE)
-----------------------------------
ANSTO's pilot-scale rare earth processing facility at Lucas Heights (Sydney) became operational in Q2 2026. It handles clay-hosted rare earths from desorption through impurity removal to separated oxide products, complementing existing hydrometallurgical and solvent extraction capabilities. The facility is open-access -- any company can bring bulk clay samples. Australian Rare Earths (AR3) is the first industry partner.

https://www.processonline.com.au/content/business/news/ar3-to-be-first-to-process-rare-earths-at-ansto-s-new-pilot-facility-1359445430


GILMOUR SPACE TECHNOLOGIES
---------------------------
No major news this week. Gilmour has confirmed TestFlight 2 (second Eris orbital attempt) is targeting late 2026 after the July 2025 failure at 14 seconds. The company is also planning a suborbital hypersonic test flight pending approvals. Block 2 Eris (1,000 kg to LEO) is in development.

Context: https://www.space.com/space-exploration/launches-spacecraft/australias-gilmour-space-not-going-to-give-up-as-it-eyes-2nd-orbital-launch-attempt-in-2026


INTUITIVE MACHINES
------------------
IM-3 (Nova-C "Trinity") is on track for H2 2026 launch to Reiner Gamma. Engineering improvements over IM-2: 12 lunar orbits before landing (vs 3), redundant laser rangefinders from two separate vendors, and an extensive crater map library integrated into landing software. Pre-flight rangefinder tests on fixed-wing aircraft and helicopters are planned.

https://aerospaceamerica.aiaa.org/how-intuitive-machines-is-planning-to-make-its-third-moon-landing-a-successful-one/


OPEN SOURCE ANGLE
-----------------
nasa/fprime -- "help wanted" issues worth looking at:
  - Catch uninitialized submodules and libraries in build system (cmake, labeled Easy First Issue)
    https://github.com/nasa/fprime/issues/5054
  - fprime-util format should work for libraries
    https://github.com/nasa/fprime/issues/4926
  - The buffer overflow bug filed May 8 (#5118) is a well-scoped fix if you know C++:
    https://github.com/nasa/fprime/issues/5118

space-ros/space-ros -- just shipped jazzy-2026.04.0; demos and simulation repos also active. Good time to try the new release and file issues.
  https://github.com/space-ros/space-ros

planetlabs/notebooks -- active this week with SuperRes examples. Jupyter-friendly, Python-based, good entry point.
  https://github.com/planetlabs/notebooks

nasa/cFE -- good-first-issue: TIME branch coverage gap
  https://github.com/nasa/cFE/issues/2695

"""

# Encode and send
raw = base64.urlsafe_b64encode(email_body.encode('utf-8')).decode('utf-8')

send_data = json.dumps({'raw': raw}).encode('utf-8')

send_req = urllib.request.Request(
    'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
    data=send_data,
    method='POST',
    headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
)

with urllib.request.urlopen(send_req) as resp:
    result = json.load(resp)

print(f"Email sent! Message ID: {result.get('id')}, Status: {result.get('labelIds')}")
