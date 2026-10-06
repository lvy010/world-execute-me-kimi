"""Kimi/Moonshot AI facts used by the on-screen technical overlays.

The values in this module are deliberately limited to public Kimi/Moonshot language so the
visual story reads as a Kimi tribute rather than a generic model demo.  Product history and
culture notes live in ``docs/KIMI_LOCALIZATION.md`` with links to the official pages.
"""

GPU = "H800"
NAME = "Kimi"
PROVIDER = "Moonshot AI"
MODEL = "Kimi K3"
MODEL_PREVIOUS = "Kimi K2.6"
TOTAL_PARAMS_B = 2800          # official K3 headline: 2.8T parameters
ACTIVE_DECODE_B = 2800         # display shorthand; K3 is presented as a 2.8T-class model
ACTIVE_PREFILL_B = 2800
PRETRAIN_TOKENS = "3T-class"
PRETRAIN_TOKENS_T = 3.0
KV_BYTES_PER_TOKEN = 1024
CTX = 1048576                  # official Kimi product limit: 1M-token context

# The config panel is a visual explainer, not a claim that every serving detail is public.
CONFIG_SOURCE = "Moonshot AI / Kimi K3"
N_LAYERS_FLASH = 61
D_MODEL = 4096
N_ROUTED = 256
N_SHARED = 1
TOP_K = 8
INDEX_TOPK = 512
SLIDING_WINDOW = 128
HC_MULT = 4
HC_SINKHORN_ITERS = 20
N_LAYERS_PRO = 61
N_ROUTED_PRO = 384
INDEX_TOPK_PRO = 1024
CONFIG_ROWS = [
    ("model", MODEL),
    ("provider", PROVIDER),
    ("context_window", "1,000,000 tokens"),
    ("vision", "native multimodal"),
    ("attention", "KDA + AttnRes"),
    ("release", "2026-07-16"),
    ("open_weights", "3T-class"),
    ("owner", '"Moonshot AI"'),
]

INIT_STD = 0.006
SEED = "curiosity"
LOSS_NOTE = "stable learning curve · long-horizon capability stays in view"
DUALPIPE_NOTE = "Kimi K3: KDA + AttnRes · attention stays useful across long tasks"
GPU_HOURS_NOTE = "Moonshot AI · open model research · science + humanism"
FS_NAME = "kimi://context"

# Serving / API language used in the assistant scenes.
DISK_CACHE_HIT = 56.3
PEAK_WINDOWS = [(9, 12), (14, 18)]
OFFPEAK_START_H = 0
OFFPEAK_END_H = 0
OFFPEAK_LABEL = "context ready · continue the thread"

# Kimi-native speculative/long-context shorthand for the animated technical overlay.
KDA_DRAFT = 5
KDA_GAIN_FLASH = "KDA · 1M context · verified continuation"
# Compatibility aliases for older scene modules.
DSPARK_DRAFT = KDA_DRAFT
DSPARK_GAIN_FLASH = KDA_GAIN_FLASH

# hakimi web / Moonshot AI surface text requested by the user.
KIMI_CMD = "hakimi web"
KIMI_TAGLINE = "Agent = Model + Harness"
KIMI_PLUGIN = "Kimi Researcher · Kimi Code · Kimi Work"
KIMI_WARNING = "CURIOUSITY NEEDS A LONG ENOUGH CONTEXT."

# The older generic reward section is reframed as agent evaluation; numbers are animation controls.
GRPO_G = 16
GRPO_KL = 0.001
GRPO_LR = "3e-6"
AHA = "Aha: the plan becomes useful when it survives the whole task."
AIME_FROM, AIME_TO = 15.6, 71.0
R1_TEMP = 0.6
R1_TOP_P = 0.95

OCR_RATIO_GOOD = (10.0, 97)
OCR_RATIO_BAD = (20.0, 60)
SLOGAN = "The Dark Side of the Moon"
RETIRED = ["kimi-k2.5-preview"]
RETIRED_DATE = "2026-07-16"
