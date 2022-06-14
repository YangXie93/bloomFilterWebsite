import streamlit as st
import numpy as np
from datasketch import HyperLogLog
import csv


# bloom filter implementation
# Generate a large stream of unique values (for example the instance ID or row ID from the dataset
# chosen under 3)) and implement a Bloom filter such that the length n can be flexibly set as a parameter.
#
# query module implementation?
# Implement a query module such that for any query key the Bloom filter reports a “miss” or a “match”.

class bloom_filter:
    
    def __init__(self,n):
        self.length = n
        self.filter = np.zeros(n)

    def reset_length(self,n):
        self.length = n
        self.filter = np.zeros(n)
        
    def hash_func(self,val):
        return int(hash(val) % self.length)
        
    def query(self,q):
        if(self.filter[self.hash_func(q)] == 1):
            return False
        else:
            self.filter[self.hash_func(q)] = 1
            return True        
        

# Implement a simple web frontend (e.g. using streamlit or svelte) to visualize the data set and set
# parameters (like Bloom filter length n and the amount of key values to insert into the Bloom filter)
# - 1 input filed for numeric (bloomfilter length)
# - visualisation of data set
#  - head table 
#  - meta data (data type, how many data points etc)
#
# For the Bloom filter, the web frontend should accept as input an arbitrary query key and display whether
# this is a true of false positive or a true negative
# - 1 input field
#
# For the count-distinct problem, the web frontend should
# display the count obtained by 5) and compare it to the real amount of distinct values
# - display 2 numbers with some text
#


#def renew_form():


st.title("Bloom Filter")
st.subheader("by Yang Xie (7405745)") 
length = 10

BF = bloom_filter(length)

length = round(st.number_input("Please enter the Bloom Filter Lenght:",value=10, on_change=BF.reset_length(length) ))
BF.reset_length(length)

number_of_querys = st.number_input("Please enter the amount of querys:",value = 1)

for i in range(0,number_of_querys):

    query = st.text_input("Query "+str(i+1)+":","1")
    result = BF.query(query)
    if(result):
        st.success("Answer: "+str(result))
    else:
        st.error("Answer: "+str(result))

source_file = csv.reader(open("/home/yang/Data/drugsComTrain_raw.tsv"),delimiter="\t")

HLL = HyperLogLog()
actual_unique = []
table = []
iterator = 0

for row in source_file:

    if( iterator < 10):
        table.append(np.array(row[:2]+row[4:]))

    
    HLL.update(row[1].encode("utf8"))
    if(not row[1] in actual_unique):
        actual_unique.append(row[1])

    iterator += 1

table = np.array(table)

st.subheader("HyperLogLog on data with variation:")
st.write("Aproximation with Hyper Loglog of unique values in the drugName column: ")
st.write(str(HLL.count()))
st.write("Actual number of unique values in the drugName column: ")
st.write(str(len(actual_unique)))
st.subheader("The data:")
st.table(table)



