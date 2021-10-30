import string
import sys

COLUMN_WIDTH = 40

def get_input_filename():
  if len(sys.argv) != 2:
    print("Usage: python3 %s <input file name>" % sys.argv[0])
    exit()
  return sys.argv[1]

def populate_word_list(input_file_name):
  words = []
  with open(input_file_name, 'r') as file:
    for line in file:
      for word in line.split():
        word = word.strip(string.punctuation + '–«»…№“’‘”').lower()
        if (len(word) > 0):
          words.append(word)
  return words

def create_frequency_histogram(word_list):
  hist = {}
  for word in word_list:
    if word in hist:
      hist[word] += 1
    else:
      hist[word] = 1
  return hist

def print_stats(word_list, hist):
  # Num words, characters, unique words
  n_chars = 0
  for word in word_list:
    n_chars += len(word)

  # Needed for median and pN calculations
  sorted_words = sorted(word_list, key=lambda x: len(x))

  print('%d words, %d characters, %d unique words' % (len(word_list), n_chars, len(hist)))
  print('Overall: %.1f avg word length, %d median word length (\'%s\'), %d p90 word length (\'%s\')' 
    % (n_chars/len(word_list), 
       len(sorted_words[int(len(sorted_words) * 0.5)-1]), 
       sorted_words[int(len(sorted_words) * 0.5)-1],
       len(sorted_words[int(len(sorted_words) * 0.9)-1]), 
       sorted_words[int(len(sorted_words) * 0.9)-1] ))
  
  n_chars = 0
  for word in hist.keys():
    n_chars += len(word)

  # NOTE: using 'reverse' so that the sort is consistent with the sort for we use in the other 
  # method for *displaying* the histogram. This way, words of same length will be in the same
  # order in both places, thus making it easier to confirm that we're doing the percentiles correctly.
  sorted_unique_words = sorted(hist.keys(), key=lambda x: len(x), reverse=True)
  print('Unique words: %.1f avg word length, %d median word length (\'%s\'), %d p90 word length (\'%s\')'
    % (n_chars/len(hist.keys()),
      len(sorted_unique_words[int(len(sorted_unique_words) * 0.5)-1]),
      sorted_unique_words[int(len(sorted_unique_words) * 0.5)-1], 
      len(sorted_unique_words[int(len(sorted_unique_words) * 0.1)-1]), # 0.1 because of reverse sort
      sorted_unique_words[int(len(sorted_unique_words) * 0.1)-1] )) # 0.1 because of reverse sort

  print('') # empty line

def print_histograms(hist):
  """Print side by side to better use the space: 
        - histogram of word counts sorted by word length
        - histogram of word counts sorted by word count
        - list of unique words in alphabetical order
  """
  keys_by_len = sorted(hist.keys(), key=lambda x: len(x), reverse=True)
  key_values_by_freq = sorted(hist.items(), key=lambda x: x[1], reverse=True)
  keys_by_alpha = sorted(hist.keys())
  
  heading1 = 'Sorted by word length'
  heading2 = 'Sorted by word frequency'
  heading3 = 'Sorted alphabetically'
  print(heading1 + ' ' * (COLUMN_WIDTH - len(heading1)) 
      + heading2 + ' ' * (COLUMN_WIDTH - len(heading2)) 
      + heading3)
  print('-' * len(heading1) + ' ' * (COLUMN_WIDTH - len(heading1)) 
      + '-' * len(heading2) + ' ' * (COLUMN_WIDTH - len(heading2)) 
      + '-' * len(heading3))

  for i in range(len(keys_by_len)):
    formatted_str1 = '%s %d' % (keys_by_len[i], hist[keys_by_len[i]])
    formatted_str1 = formatted_str1 + ' ' * (COLUMN_WIDTH - len(formatted_str1))
    formatted_str2 = '%s %d' % (key_values_by_freq[i][0], key_values_by_freq[i][1])
    formatted_str2 = formatted_str2 + ' ' * (COLUMN_WIDTH - len(formatted_str2))
    formatted_str3 = keys_by_alpha[i]
    print(formatted_str1 + formatted_str2 + formatted_str3)

############################## MAIN ##############################
word_list = populate_word_list(get_input_filename())
hist = create_frequency_histogram(word_list)
print_stats(word_list, hist)
print_histograms(hist)
