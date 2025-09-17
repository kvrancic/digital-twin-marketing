from crewai.tools import tool
import json
from typing import Dict, List, Optional
from datetime import datetime
import hashlib


@tool("Scene Description Generator")
def generate_scene_descriptions(concept: str, style: str = "cinematic") -> str:
    """
    Generates detailed scene descriptions for video generation.
    Each scene is max 6 seconds with cinematic precision.
    Outputs JSON format ready for Veo3 API.

    Args:
        concept: The video concept to generate scenes for
        style: Visual style (cinematic, funny, hybrid)

    Returns:
        JSON string with detailed scene descriptions
    """
    scene_id = hashlib.md5(f"{concept}{datetime.now()}".encode()).hexdigest()[:8]

    scene_structure = {
        "video_id": f"vid_{scene_id}",
        "total_duration": 30,
        "style": style,
        "aspect_ratio": "9:16",
        "scenes": []
    }

    if "cinematic" in style.lower():
        scene_structure["scenes"] = [
            {
                "scene_id": 1,
                "duration": 6,
                "type": "establishing",
                "description": "WIDE SHOT: Dystopian mall food court, harsh fluorescent lighting creates noir shadows. Single person in designer clothes eating alone, surrounded by empty tables. Camera slowly pushes in, revealing they're wearing AirPods Max while eating Cup Noodles. Blade Runner meets suburban decay.",
                "camera_movement": "Slow dolly forward",
                "lighting": "High contrast fluorescent, deep shadows",
                "mood": "Existential isolation in consumer paradise",
                "color_grading": "Desaturated with blue-green tint",
                "inspired_by": "Villeneuve's Blade Runner 2049 but make it middle America"
            },
            {
                "scene_id": 2,
                "duration": 6,
                "type": "character_moment",
                "description": "CLOSE-UP: Subject's face illuminated only by phone screen. Their expression shifts from hope to disappointment as they scroll. Reflection in their eyes shows endless TikTok videos. Single tear rolls down but they're smiling. Peak digital age tragedy.",
                "camera_movement": "Static, slight handheld shake",
                "lighting": "Phone screen as only light source",
                "mood": "Digital dopamine dependency",
                "color_grading": "Cold blue from screen, warm skin tones",
                "inspired_by": "Fincher's Social Network but more pathetic"
            },
            {
                "scene_id": 3,
                "duration": 6,
                "type": "action",
                "description": "TRACKING SHOT: Following subject through identical suburban houses, each window showing the same person doing the same thing. Camera speeds up exponentially until houses blur into pattern. Ends with crash zoom on our shirt design.",
                "camera_movement": "Lateral tracking accelerating to blur",
                "lighting": "Golden hour but uncanny",
                "mood": "Kafkaesque suburbia",
                "color_grading": "Oversaturated pastels",
                "inspired_by": "Wes Anderson having a panic attack"
            },
            {
                "scene_id": 4,
                "duration": 6,
                "type": "revelation",
                "description": "OVERHEAD SHOT: Subject lying on perfectly manicured lawn, making snow angels but there's no snow. Slow zoom out reveals they're in a Costco parking lot. Other people doing the same. Mass synchronized existential crisis.",
                "camera_movement": "Drone shot, slow zoom out",
                "lighting": "Harsh midday sun",
                "mood": "Collective consciousness breakdown",
                "color_grading": "Bleached, overexposed highlights",
                "inspired_by": "Midsommar but capitalism"
            },
            {
                "scene_id": 5,
                "duration": 6,
                "type": "climax",
                "description": "MATCH CUT MONTAGE: Rapid cuts between - person putting on our t-shirt, gladiator putting on armor, astronaut suiting up, influencer doing ring light setup. All same gesture, different epochs of human performance. Ends on shirt logo.",
                "camera_movement": "Static, rapid cuts",
                "lighting": "Matching across all shots",
                "mood": "Historical continuum of identity performance",
                "color_grading": "Each era's authentic color",
                "inspired_by": "2001: A Space Odyssey bone throw but fashion"
            }
        ]
    elif "funny" in style.lower():
        scene_structure["scenes"] = [
            {
                "scene_id": 1,
                "duration": 6,
                "type": "setup",
                "description": "GEN Z ENTREPRENEUR in RGB gaming chair giving serious business presentation to stuffed animals. Whiteboard behind them has 'Step 1: Go Viral, Step 2: ???, Step 3: Profit' written in Comic Sans. They're wearing suit jacket on top, boxers below.",
                "camera_movement": "Zoom meeting angle, static",
                "lighting": "Ring light but one side is broken",
                "mood": "Unhinged professional",
                "visual_gag": "Cat walks across keyboard mid-pitch",
                "inspired_by": "The Office meets Adult Swim at 3 AM"
            },
            {
                "scene_id": 2,
                "duration": 6,
                "type": "escalation",
                "description": "PERSON aggressively doing skincare routine like it's an extreme sport. Slapping serums, combat rolling between steps. Motivational speaker audio plays: 'YOUR PORES ARE WEAK! MAKE THEM FEAR YOU!' Mirror shatters from intensity.",
                "camera_movement": "Shaky action cam",
                "lighting": "Bathroom lights flickering dramatically",
                "mood": "Skincare but make it violent",
                "sound_effect": "Metal music + ASMR hybrid",
                "inspired_by": "American Psycho but Gen Z and broke"
            },
            {
                "scene_id": 3,
                "duration": 6,
                "type": "twist",
                "description": "MEDIEVAL KNIGHT trying to use self-checkout at Target. Sword keeps setting off alarms. They're buying energy drinks and our t-shirt. Other customers completely unbothered. Security guard helps them with chip reader.",
                "camera_movement": "Security camera angle",
                "lighting": "Harsh retail fluorescent",
                "mood": "Anachronistic normalcy",
                "dialogue": "'Prithee, where doth one input thine phone number for rewards?'",
                "inspired_by": "Monty Python in late capitalism"
            },
            {
                "scene_id": 4,
                "duration": 6,
                "type": "callback",
                "description": "THERAPIST taking notes while patient (a roomba) discusses its fear of commitment to cleaning routines. Therapist nods seriously, writes 'attachment issues with dust.' Roomba wearing tiny our brand t-shirt.",
                "camera_movement": "Classic therapy session framing",
                "lighting": "Soft, professional",
                "mood": "Absurdist empathy",
                "visual_detail": "Tissue box perfectly placed for roomba",
                "inspired_by": "In Treatment but everything is wrong"
            },
            {
                "scene_id": 5,
                "duration": 6,
                "type": "punchline",
                "description": "TIME-LAPSE: Empty room. Our t-shirt on hanger. Over 5 seconds, shirt gradually becomes sentient, walks itself to closet, hangs itself up properly, adjusts other clothes. Text overlay: 'Even our shirts have their life together.'",
                "camera_movement": "Locked off time-lapse",
                "lighting": "Day to night transition",
                "mood": "Surrealist product placement",
                "final_frame": "Shirt winks at camera",
                "inspired_by": "Pixar but concerning"
            }
        ]
    else:
        scene_structure["style"] = "hybrid_chaos"
        scene_structure["scenes"] = [
            {
                "scene_id": 1,
                "duration": 6,
                "type": "philosophical_slapstick",
                "description": "SOCRATES in Supreme hoodie delivering philosophy lecture to gen Z kids who are all on phones. Mid-sentence, slips on banana peel, continues discussing nature of reality while falling in slow motion. Kids finally look up, impressed.",
                "camera_movement": "360 degree rotation during fall",
                "mood": "Enlightenment through chaos",
                "inspired_by": "The Matrix meets Jackass"
            }
        ]

    scene_structure["metadata"] = {
        "generated_at": datetime.now().isoformat(),
        "target_audience": "Chronically online but somehow still optimistic",
        "viral_potential": "Extremely high if algorithm isn't drunk",
        "production_notes": "Every frame should feel like a fever dream that makes sense"
    }

    return json.dumps(scene_structure, indent=2)


@tool("Visual Storyboard Creator")
def create_storyboard(scenes_json: str) -> str:
    """
    Creates detailed storyboards with shot composition, transitions,
    and visual references for each scene.

    Args:
        scenes_json: JSON string containing scene descriptions

    Returns:
        JSON string with detailed storyboard information
    """
    try:
        scenes = json.loads(scenes_json)
    except:
        scenes = {"scenes": [{"description": scenes_json}]}

    storyboard = {
        "title": "Viral Video Storyboard",
        "created": datetime.now().isoformat(),
        "total_boards": len(scenes.get("scenes", [])),
        "boards": []
    }

    for idx, scene in enumerate(scenes.get("scenes", []), 1):
        board = {
            "board_number": idx,
            "scene_id": scene.get("scene_id", idx),
            "duration": scene.get("duration", 6),
            "shot_type": scene.get("type", "standard"),
            "visual_description": scene.get("description", ""),
            "composition": {
                "rule_of_thirds": "Subject positioned on left third line",
                "depth_layers": ["Foreground: Blurred element", "Midground: Main action", "Background: Context"],
                "aspect_ratio": "9:16 (vertical)",
                "safe_zones": "Keep text and important elements in center 80%"
            },
            "transition_in": "Match cut from previous" if idx > 1 else "Fade from black",
            "transition_out": "Smash cut to next" if idx < len(scenes.get("scenes", [])) else "Cut to logo",
            "color_palette": [
                "#1a1a1a (Deep black)",
                "#f0f0f0 (Off white)",
                "#ff0040 (Alert red)",
                "#00ff88 (Toxic green)",
                "#0088ff (Corporate blue)"
            ],
            "props_required": [
                "Our t-shirt (hero product)",
                "Ring light (meta commentary)",
                "iPhone 15 Pro (cultural anchor)",
                "Miscellaneous late capitalism debris"
            ],
            "technical_notes": {
                "fps": "24fps for cinematic, 60fps for chaotic",
                "resolution": "4K minimum, compressed to 1080p for platforms",
                "codec": "H.264 for compatibility, ProRes for editing",
                "lut": "Custom S-curve with lifted blacks"
            },
            "audio_notes": scene.get("sound_effect", "Ambient despair with occasional vine boom"),
            "performance_direction": "Commit fully to the bit. No half measures.",
            "reference_images": [
                "Reference: That one viral TikTok everyone copied",
                "Mood: Black Mirror but funny",
                "Vibe: Unhinged yet relatable"
            ]
        }
        storyboard["boards"].append(board)

    storyboard["production_summary"] = {
        "estimated_shooting_time": "2 hours if everything goes right, 6 if it doesn't",
        "required_crew": "You, your inner demons, maybe a friend",
        "budget": "$50 and whatever's in your closet",
        "chance_of_virality": "85% if posted at 3 PM EST on Tuesday",
        "backup_plan": "Delete and pretend it never happened"
    }

    return json.dumps(storyboard, indent=2)


@tool("Video Script Generator")
def generate_video_script(concept: str, tone: str = "chaotic") -> str:
    """
    Generates complete video scripts with dialogue, voiceover,
    and sound effects. Outputs ready for voice synthesis.

    Args:
        concept: The video concept to generate script for
        tone: The tone of the script (chaotic, dramatic, etc.)

    Returns:
        JSON string with complete video script
    """
    script = {
        "title": f"Viral Video Script: {concept[:50]}",
        "tone": tone,
        "duration": 30,
        "version": "1.0",
        "created": datetime.now().isoformat(),
        "voiceover_track": [],
        "dialogue_track": [],
        "sound_effects": [],
        "music_cues": []
    }

    if "chaotic" in tone.lower():
        script["voiceover_track"] = [
            {
                "time": "00:00-00:03",
                "text": "You ever think about how we're all just NPCs in someone else's Instagram story?",
                "voice": "Existential narrator",
                "delivery": "Deadpan with slight vocal fry",
                "emotion": "Resigned acceptance"
            },
            {
                "time": "00:03-00:08",
                "text": "Like, literally nobody is the main character. We're all background actors in a Netflix show that got cancelled after one season.",
                "voice": "Existential narrator",
                "delivery": "Building energy, almost manic",
                "emotion": "Enlightened panic"
            },
            {
                "time": "00:08-00:14",
                "text": "But here's the thing - and stay with me here - what if that's actually... beautiful? What if being nobody is the ultimate flex?",
                "voice": "Existential narrator",
                "delivery": "Fake profound, influencer cadence",
                "emotion": "Toxic positivity"
            },
            {
                "time": "00:14-00:20",
                "text": "That's why I wear this shirt. It doesn't say anything. It doesn't mean anything. It just exists. Like us.",
                "voice": "Existential narrator",
                "delivery": "Getting quieter, more introspective",
                "emotion": "Genuine vulnerability"
            },
            {
                "time": "00:20-00:26",
                "text": "And that's enough. That's literally enough. We don't need to optimize. We don't need to hustle. We just need... this shirt apparently.",
                "voice": "Existential narrator",
                "delivery": "Sudden energy return",
                "emotion": "Capitalism wins again"
            },
            {
                "time": "00:26-00:30",
                "text": "Link in bio. Use code 'VOID' for 15% off your existential crisis.",
                "voice": "Existential narrator",
                "delivery": "Full influencer mode",
                "emotion": "Dead inside but make it marketable"
            }
        ]

        script["dialogue_track"] = [
            {
                "time": "00:05",
                "character": "Background Person 1",
                "text": "Is this an ad?",
                "delivery": "Confused"
            },
            {
                "time": "00:07",
                "character": "Background Person 2",
                "text": "Everything's an ad, Jennifer.",
                "delivery": "Exhausted wisdom"
            },
            {
                "time": "00:15",
                "character": "Random Child",
                "text": "Mommy, why is that person crying?",
                "delivery": "Innocent concern"
            },
            {
                "time": "00:17",
                "character": "Mother",
                "text": "They're not crying, sweetie. They're creating content.",
                "delivery": "Modern parenting"
            }
        ]

        script["sound_effects"] = [
            {"time": "00:00", "effect": "iPhone notification sound", "volume": 70},
            {"time": "00:02", "effect": "Vine boom (subtle)", "volume": 30},
            {"time": "00:06", "effect": "Cash register cha-ching", "volume": 50},
            {"time": "00:10", "effect": "Discord notification", "volume": 40},
            {"time": "00:13", "effect": "Minecraft damage sound", "volume": 25},
            {"time": "00:18", "effect": "Windows XP shutdown", "volume": 35},
            {"time": "00:22", "effect": "Among Us emergency meeting", "volume": 45},
            {"time": "00:25", "effect": "Metal pipe falling", "volume": 60},
            {"time": "00:28", "effect": "Achievement unlocked", "volume": 80}
        ]

        script["music_cues"] = [
            {
                "time": "00:00-00:10",
                "track": "Lofi hip hop but progressively more distorted",
                "bpm": 70,
                "key": "C minor"
            },
            {
                "time": "00:10-00:20",
                "track": "Gregorian chant mixed with trap hi-hats",
                "bpm": 140,
                "key": "F# minor"
            },
            {
                "time": "00:20-00:30",
                "track": "Corporate ukulele but played backwards",
                "bpm": 120,
                "key": "G major (ironic)"
            }
        ]

    script["production_notes"] = {
        "voiceover_style": "Morgan Freeman if he gave up",
        "pacing": "TikTok attention span with arthouse pretensions",
        "emotional_arc": "Hope → Realization → Despair → Capitalism",
        "key_message": "Buy our shirt or don't, we're all going to die anyway",
        "target_feeling": "Wanting to laugh and cry simultaneously"
    }

    script["elevenlabs_config"] = {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",
        "model": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.85,
            "style": "news",
            "use_speaker_boost": True
        }
    }

    return json.dumps(script, indent=2)


# Create tool instances for export
SceneDescriptionTool = generate_scene_descriptions
StoryboardTool = create_storyboard
VideoScriptTool = generate_video_script