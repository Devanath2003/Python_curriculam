
import logging 
def setup_logger(name:str = "spendsense") -> logging.Logger :

    logging.basicConfig(
        level= logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler("app.log", encoding="utf-8"),
            logging.StreamHandler()
        ]

    )

    logger = logging.getLogger(name)

    return logger


if __name__ == "__main__":

    a = 5

    lor = setup_logger("checker")

    if a > 2:
        lor.warning("It's an invalid number: %s",a)

    if a < 6:
        lor.info("It's safe: %s",a)
