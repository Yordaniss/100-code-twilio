# The repository for confirmation the code 100 challenge.

Using the examples I wrote the code that decides which encoding method was used and how many bits was used.

Additional to this I wrote the logic to determine the hash, bit counts and some additional information and this will be written into csv file. Also how much sms should be send according to number of charachters.

To test this one, I wrote also test class with examples above and expecting outputs. 

Steps to solve the challenge:

- Get all charachters and check if there are charachters for UCS-2 decoding. Otherwise GSM-7
- If GSM-7 use counting logic to determine at the end, how much bits would be used
- In UCS-2 I wrote additional method to get length of bits from the text.
- Then also write the outputs into csv
- To check if the logic works I wrote tests with examples from challenges.
