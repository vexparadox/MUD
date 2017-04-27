worldmap = {
	'width': 3,
	'height': 2,
	'worldmap':[
		{
			'id': 0,
			'title': 'Gwynhaven',
			'description': 'A small, humble town where heroes seem to be born daily.',
			'here': 'You take a look around, this is a small town that likes to keep up appearances. In the middle of the square you see a message board onto which others have scribed inspirational messages.\nOn the edge of town there\'s a small band of tired soldiers, they have a mysterious yellow exclamation mark above their heads.',
			'n': 'To the north you see the world falling away into a dark void, it turns your stomach.',
			'e': 'To the east you can see a small path winding through a forest.',
			's': 'Turning to the south you see a thick forest, it\'s impassable without some tools.',
			'w': 'Looking to the west you see a vast expanse of nothingness, you feel dizzy and turn away.',
			'requireditems': [],
			'passable': 'true'
		},
		{
			'id': 1,
			'title': 'Forest path',
			'description': 'A heavily trodden path through the forest, the air carries palpable tension.',
			'here': 'There\'s something eary about this place... You smell the sweat of Golbins.',
			'n': 'To the north you see the world falling away, you wonder how this place came to be.',
			'e': 'You turn to the east, you can see a small settlement in the distance.',
			's': 'The thick forest continues, it looks more alive than you expected.',
			'w': 'Turning to the west you see the town of Gwynhaven, you smile at the thought of humble beginnings.',
			'requireditems': [], 
			'passable': 'true'
		},
		{
			'id': 2,
			'title': 'Crattelish Outpost',
			'description': 'An outpost manned by the proud but fickle Crattelish people.',
			'here': 'This place feels safe. There\'s a message board on the side of a hut, it has messages left by other travellers.\nTaking a closer look there\'s also some job postings.' ,
			'n': 'To the north the ground slips away into the void.',
			'e': 'The east carries a sense of danger, you decide to go another day.',
			's': 'Looking to the south you see a break in the thick forest, there seems to be a path.',
			'w': 'To the west you see a well trodden forest path, it seems to lead to Gwynhaven.',
			'requireditems': [],
			'passable': 'true'
		},
		{
			'id': 3,
			'title': 'Farghen Forest',
			'description': 'A dense forest, older than the town of Gwynhaven it was .',
			'here': 'The ground moves as you walk over it, the air is thick with life.' ,
			'n': 'To the north you can see the town of Gwynhaven, the feeling of home gives you warmth.',
			'e': 'The east carries the forest further.',
			's': 'The south is impassable, once again the black has caught up to you.',
			'w': 'Turning to the west you see the face of the void, it stares back.',
			'requireditems': ['cut'], # Requires a machete
			'passable': 'true'
		},
		{
			'id': 4,
			'title': 'Fargen Forest Outskirts',
			'description': 'The outskirts of the Fargen Forest.',
			'here': 'This place feels safe. There\'s a message board on the side of a hut, it has messages left by other travellers.\nTaking a closer look there\'s also some job postings.' ,
			'n': 'Over the hill to the north you see the Forest Path, you\'re annoyed at how easy it was to walk.',
			'e': 'To the east there\'s a path lined with guards, they seem stiff.',
			's': 'The south sees the world fall away into black, you turn away.',
			'w': 'Turning to the west you see the forest continue.',
			'requireditems': ['cut'], # Requires a machete
			'passable': 'true'
		},
		{
			'id': 5,
			'title': 'Crattelish Forest Path',
			'description': 'A small winding path through the dense forest.',
			'here': 'Guards are dotted around the tree line, they seem indifferent to the rustling behind them.' ,
			'n': 'To the north you see smoke rising about the Crattelish Outpost.',
			'e': 'The east gives you a sense of dread, past the trees you see the dark.',
			's': 'Looking to the south you see COMING SOON LOL.',
			'w': 'The west is walled by an indescribably thick forest, you\'ll need tools to get through there.',
			'requireditems': [], # Requires a machete
			'passable': 'true'
		},
	],
}