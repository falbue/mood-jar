import config

if __name__ == "__main__":
    from TelegramTextApp import TTA
    TTA.start(
      config.API,
      "menus",
      debug=True,
      tta_experience=True
    )