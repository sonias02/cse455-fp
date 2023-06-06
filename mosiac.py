import numpy as np
from PIL import Image
import os

# ---- Credits ----
# default big image from https://www.almanac.com/plant/roses
# small images from https://www.kaggle.com/datasets/alxmamaev/flowers-recognition

# ---- Variables ----
# initalized based on chosen big image and size
BIG_IMAGE = None
SIZE = None
NUM_IMAGES_WIDTH = None
NUM_IMAGES_HEIGHT = None

# ---- Helper functions ----
def askForInput():
  """ Sets up mosiac based on user input
    Takes in user input to decide what the big images will be and what size the smaller images will be
    The default big image is "rose.jpg" with a size of 10
  """
  global BIG_IMAGE, SIZE
  print(">>\n>> Welcome to the mosiac creater! We will take your image and create a mosiac of it using rose images.")
  isPersonalized = input(">> The default image is a rose and size 10, but do you want to input a personalized image or size? (yes/no)\n>> ").lower()

  isReady = False
  while not isReady:
    if isPersonalized == "yes":
      # get file name
      file = input(">>\n>> Enter a file name for your image (.jpg, we recommend 500 pixels or less):\n>> ")
      try:
        BIG_IMAGE = Image.open(file)
      except:
        print(">> Error: File does not exist in this directory, please try again.")
        continue

      # get size
      while True:
        try:
          size = int(input(">>\n>> Enter a size between 5 and 20 (we recommend smaller sizes for more detailed images):\n>> "))
          if (size >= 5 and size <= 20):
            SIZE = int(size)
            isReady = True
            break
          else:
            print(">> Error: Enter a valid size between 5 and 30, please try again.")
        except:
          print(">> Error: Enter a valid integer, please try again.")
    elif isPersonalized == "no":
      # set image and size to default values
      BIG_IMAGE = Image.open("rose.jpg")
      SIZE = 10
      isReady = True
    else:
        print(">> Error: Please respond with yes or no.")
  print(">>\n>> Creating a mosaic with", BIG_IMAGE.filename, "...")


def pixelateBigImage(big_image):
  """ Pixelates given image
    Chooses every SIZE pixels from the big image to create a new image
    The pixels represent where each of the smaller images will be
    Calculates NUM_IMAGES_WIDTH and NUM_IMAGES_HEIGHT

    :param big_image: the original big image
    :return: a new image that is the same size as BIG_IMAGE but has fewer pixels
  """
  global NUM_IMAGES_WIDTH, NUM_IMAGES_HEIGHT

  # choose pixels
  image_array = np.asarray(big_image)
  pixels = image_array[::SIZE,::SIZE]

  # create new image
  new_big_image = Image.fromarray(pixels)
  NUM_IMAGES_WIDTH = int(new_big_image.size[0])
  NUM_IMAGES_HEIGHT = int(new_big_image.size[1])
  return new_big_image.resize((NUM_IMAGES_WIDTH*SIZE, NUM_IMAGES_HEIGHT*SIZE))


def getSmallImages():
  """ Returns filenames for the smaller images

    :return: an array of filenames of the smaller rose images
  """
  images = []
  for image in os.listdir("./roses"):
    images.append(image)
  return images


def createCollage(images):
  """ Returns collage of small images

    :param images: array of image filenames
    :return: an image of all the smaller images put together
  """
  # create rows
  rows = []
  for h in range(NUM_IMAGES_HEIGHT):
    for w in range(NUM_IMAGES_WIDTH):
      # get image
      i = h * NUM_IMAGES_WIDTH + w
      image = images[i % len(images)]
      image = Image.open("./roses/" + image)
      image = image.resize((SIZE, SIZE))

      # create new row and merge
      if w == 0:
        merged_row = image
      else:
        new_row = Image.new('RGB',(merged_row.size[0] + SIZE, SIZE), (250,250,250))
        new_row.paste(merged_row,(0,0))
        new_row.paste(image,(merged_row.size[0], 0))
        merged_row = new_row
    rows.append(merged_row)

  # merge rows
  merged_image = None
  for i, row in enumerate(rows):
    if i == 0:
      merged_image = row
    else:
      new_image = Image.new('RGB',(merged_image.size[0], merged_image.size[1] + SIZE), (250,250,250))
      new_image.paste(merged_image,(0,0))
      new_image.paste(row,(0, merged_image.size[1]))
      merged_image = new_image

  return merged_image


def blend(collage, big_image):
  """ Blends the two given images together

    :param collage: collage of small images
    :param big_image: pixelated big image
    :return: image that is a blend of the given big image and collage
  """
  collage = collage.convert("RGBA")
  big_image = big_image.convert("RGBA")
  return Image.blend(collage, big_image, alpha=0.6)

# ---- Create mosiac ----
askForInput()
BIG_IMAGE = pixelateBigImage(BIG_IMAGE)
images = getSmallImages()
collage = createCollage(images)
blended = blend(collage, BIG_IMAGE)
blended.show()