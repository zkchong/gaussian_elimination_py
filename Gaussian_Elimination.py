# 
#import bitarray
#from BitVector import BitVector
from bitstring import BitArray
import copy
#-----------------------------------------------------------------------
__VERSION__ = '21-Nov-2014'
#-----------------------------------------------------------------------

#
# The input_generator_bv 
#
DEBUG = False
class Gaussian_Elimination:
    @classmethod
    def form_triangle_matrix(self, input_generator_bitarr_list, input_data_bitarr_list = None):
        
        generator_bitarr_list = copy.copy(input_generator_bitarr_list)
        data_bitarr_list = copy.copy(input_data_bitarr_list)
        
        if data_bitarr_list != None:
            # Both generator and data should ahve the same row dimensions.
            assert (len (generator_bitarr_list) == len(data_bitarr_list) )
        
        triangle_generator_bitarr_list = []
        triangle_data_bitarr_list = []
        
        for pivot in range(len(generator_bitarr_list[0])):
            # 1. Search for candidate row
            if DEBUG: print ('Step 1: Search for candidate row.')
            candidate_generator = None
            candidate_data = None
            
            for i in range(len(generator_bitarr_list)):
                g = generator_bitarr_list[i]
                if g[pivot] == 1: # Found the candidate
                    candidate_generator = generator_bitarr_list[i]
                    if input_data_bitarr_list:
                        candidate_data = data_bitarr_list [i]
                    
                    # Remove the candidate from the list
                    generator_bitarr_list.pop(i)
                    if input_data_bitarr_list:
                        data_bitarr_list.pop(i)
                    break
            
            if DEBUG: print ('Selected candidate_generator = %s' % candidate_generator)
            if DEBUG: print ('Selected candidate_data = %s' % candidate_data)
            
            # Return error in term of None if cannot find any candidate.
            if candidate_generator is None:
                if input_data_bitarr_list:
                    return None, None
                else:
                    return None
            
            triangle_generator_bitarr_list.append(candidate_generator)
            triangle_data_bitarr_list.append(candidate_data)
            
            if DEBUG: print ('triangle_generator_bitarr_list = %s' % triangle_generator_bitarr_list)
            if DEBUG: print ('triangle_data_bitarr_list = %s' % triangle_data_bitarr_list)
            
            # 2. Clean all the rows that have 1 in pivot entry.
            if DEBUG: print ('Step 2: Clean all the rows that have 1 in pivot entry.')
            for i in range(len(generator_bitarr_list)):
                if generator_bitarr_list[i][pivot] == 1:
                    generator_bitarr_list[i] = generator_bitarr_list[i].__xor__(candidate_generator)
                    if input_data_bitarr_list:
                        data_bitarr_list[i] = data_bitarr_list[i].__xor__(candidate_data)
                        
        if DEBUG: print ('triangle_generator_bitarr_list = %s' % triangle_generator_bitarr_list)
        if DEBUG: print ('triangle_data_bitarr_list = %s' % triangle_data_bitarr_list)
        
        if input_data_bitarr_list:
            return triangle_generator_bitarr_list, triangle_data_bitarr_list
        else:
            return triangle_generator_bitarr_list

    #
    #
    #
    @classmethod
    def solve_triangle_matrix(self,input_generator_bitarr_list, input_data_bitarr_list = None):
        
        generator_bitarr_list = copy.copy(input_generator_bitarr_list)
        data_bitarr_list =  copy.copy(input_data_bitarr_list)
        
        for pivot in reversed(range(len(generator_bitarr_list))):
            assert (generator_bitarr_list[pivot][pivot] == 1)
                
            for i in reversed(range( pivot )):
                if generator_bitarr_list[i][pivot] == 1:
                    generator_bitarr_list[i] = generator_bitarr_list[i].__xor__(generator_bitarr_list[pivot])
                    if data_bitarr_list:
                        data_bitarr_list[i] = data_bitarr_list[i].__xor__(data_bitarr_list[pivot])
        
        if data_bitarr_list:
            return generator_bitarr_list, data_bitarr_list
        else:
            return generator_bitarr_list

#-----------------------------------------------------------------------


#-----------------------------------------------------------------------
# For testing.
#-----------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    #from pprint import pprint
    #-------------------------------------------------------------------
    # Necessary function
    #-------------------------------------------------------------------
    
    #
    # To generate Random code's coded symbols. 
    #
    def generate_coded_symbol(generator_row, message_symbol_list):
        assert (len(generator_row) == len(message_symbol_list))
        
        selected_list = [message_symbol_list[i] for i, g in enumerate(generator_row) if g == 1]
        
        #coded_symbol = bitarray.bitarray('0' * len(message_symbol_list[0]))
        #coded_symbol = BitVector(size = len(message_symbol_list[0]))
        coded_symbol = BitArray( [0] * len(message_symbol_list[0]) )
        for s in selected_list:
            coded_symbol = coded_symbol.__xor__(s)
        
        return coded_symbol
    
    #
    # To print the list in a nice format
    # 
    def print_list(input_list):
        for i, g in enumerate(input_list):
            print ('[%02d]: %s' % (i, g.bin) )  
    
    #-------------------------------------------------------------------
    
    import random
    
    randnum = random.randint(0,100000)
    random.seed(randnum)
    print ('randnum = %d' % randnum)
    
    # Data
    total_message_symbol = 10 # This message has $total_message_symbol symbols.
    message_symbol_size = 20  # The message symbol has $message_symbol_size bits.
    
    # Total generator row to generate.
    total_generator_row = total_message_symbol + 10 # I will generate k+10 rows.
    
    generator_bitarr_list = []
    data_bitarr_list = []
    coded_symbol_bitarr_list = []
    
    #
    # Generate message symbols.
    #
    for i in range(total_message_symbol):
        #data = [random.choice([0, 1]) for i in range(message_symbol_size) ]
        #data_bv = BitVector(size=0).gen_rand_bits_for_prime(message_symbol_size) # This one doesn't work correctly.
        #data_bv = BitVector(bitlist = [random.choice([0, 1]) for i in range(message_symbol_size) ])
        data_bitarr = BitArray([random.choice([0, 1]) for i in range(message_symbol_size) ])
        #data_bitarr_list.append(bitarray.bitarray (data_bv))
        data_bitarr_list.append(data_bitarr)
    
    #
    # Generate generator_bitarr_list and coded_symbol_bv_list.
    #
    for i in range(total_generator_row):
        #new_list = [random.choice([0, 1]) for i in range(total_message_symbol) ]
        #generator = bitarray.bitarray (new_list)
        #generator_bv =  BitVector(size=0).gen_rand_bits_for_prime(total_message_symbol)
        #generator_bv = BitVector(bitlist = [random.choice([0, 1]) for i in range(total_message_symbol) ])
        generator_bitarr = BitArray([random.choice([0, 1]) for i in range(total_message_symbol) ])
        generator_bitarr_list.append( generator_bitarr )
        
        coded_symbol_bitarr_list.append( generate_coded_symbol(generator_bitarr, data_bitarr_list) )
    
    #
    # Report
    #
    print ('#------------------------------------------------------------')
    print ('Sage 0: Original data')
    print ('#------------------------------------------------------------')
    
    print ('data_bitarr_list :')
    print_list (data_bitarr_list)
    print 
    
    print ('generator_bitarr_list :')
    print_list (generator_bitarr_list)
    print 
    
    print ('coded_symbol_bitarr_list :')
    print_list (coded_symbol_bitarr_list)
    print 

    
    print ('#------------------------------------------------------------')
    print ('Step 1: GE''s form_triangle_matrix')
    print ('#------------------------------------------------------------' )
    
    s1_generator_bitarr_list, s1_coded_symbol_bitarr_list = Gaussian_Elimination.form_triangle_matrix(generator_bitarr_list, coded_symbol_bitarr_list)
    s1_generator_bitarr_list_temp = Gaussian_Elimination.form_triangle_matrix(generator_bitarr_list)
    
    # to ensure coded_symbol can be removed from form_triangle_matrix function.
    assert (s1_generator_bitarr_list == s1_generator_bitarr_list_temp)
   
    print ('generator_bitarr_list :')
    print_list (generator_bitarr_list)
    
    if  s1_generator_bitarr_list is None:
        print ('Cannot solve.')
        sys.exit(-1)
    
    print ('s1_generator_bitarr_list :')
    print_list (s1_generator_bitarr_list)
    print 
    
    print ('s1_coded_symbol_bitarr_list :')
    print_list (s1_coded_symbol_bitarr_list)
    print 
    
    
    print ('#------------------------------------------------------------')
    print ('Sage 2: After solve_triangle_matrix')
    print ('#------------------------------------------------------------' )  

    s2_generator_bitarr_list, s2_coded_symbol_bitarr_list  = Gaussian_Elimination.solve_triangle_matrix(s1_generator_bitarr_list, s1_coded_symbol_bitarr_list)
    s2_generator_bitarr_list_temp  = Gaussian_Elimination.solve_triangle_matrix(s1_generator_bitarr_list)
    
    assert (s2_generator_bitarr_list == s2_generator_bitarr_list_temp)
    
    print ('s2_generator_bitarr_list :')
    print_list (s2_generator_bitarr_list)
    print 
    
    print ('s2_coded_symbol_bitarr_list :')
    print_list (s2_coded_symbol_bitarr_list)
    print 
    
    print ('#------------------------------------------------------------')
    print ('Sage 3: Verification')
    print ('#------------------------------------------------------------')

    if s2_coded_symbol_bitarr_list == data_bitarr_list:
        print ('Encoding and Decoding: Success!')
    else:
        print ('Encoding and Decoding: Fail!')
