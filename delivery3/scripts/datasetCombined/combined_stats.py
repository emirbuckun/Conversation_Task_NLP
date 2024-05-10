""" 
This script calculates the statistics of the combined dataset and writes them to a file.
"""

import statistics
import json

# open the combined json file
with open("combined.json", "r", encoding="utf-8") as f:
    data = json.load(f) # returns JSON object as a dictionary

# pylint: disable-msg=C0103
# instructionCount is the number of instructions in the dataset
instructionCount = 0

# initialize lists to store the lengths of the instructions, inputs, and outputs
instructionLengths = []
inputLengths = []
outputLengths = []

# iterate through the combined dataset
for row in data:
    instructionCount += 1
    instructionLengths.append(len(row["instruction"]))
    inputLengths.append(len(row["input"]))
    outputLengths.append(len(row["output"]))

# calculate average lengths
avgInstructionLength = statistics.mean(instructionLengths)
avgInputLength = statistics.mean(inputLengths)
avgOutputLength = statistics.mean(outputLengths)

# calculate standard deviations
stdDevInstruction = statistics.stdev(instructionLengths)
stdDevInput = statistics.stdev(inputLengths)
stdDevOutput = statistics.stdev(outputLengths)

# open the combined_stats.txt file and write the stats
with open("combined_stats.txt", "w", encoding="utf-8") as f:
    f.write("Number of instructions: " + str(instructionCount) + "\n")
    f.write("\n")
    f.write("Average instruction length: " + str(avgInstructionLength) + "\n")
    f.write("Average input length: " + str(avgInputLength) + "\n")
    f.write("Average output length: " + str(avgOutputLength) + "\n")
    f.write("\n")
    f.write("Standard deviation of instruction length: " + str(stdDevInstruction) + "\n")
    f.write("Standard deviation of input length: " + str(stdDevInput) + "\n")
    f.write("Standard deviation of output length: " + str(stdDevOutput) + "\n")
