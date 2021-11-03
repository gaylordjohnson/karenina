import string
import sys

COLUMN_WIDTH = 35

def get_input_filename():
  if len(sys.argv) != 2:
    print('Usage: python3 %s <input file name>' % sys.argv[0])
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

def create_histograms(words):
  word_hist = {}
  char_hist = {}
  for word in words:
    if word in word_hist:
      word_hist[word] += 1
    else:
      word_hist[word] = 1

    for ch in word:
      if ch in char_hist:
        char_hist[ch] += 1
      else:
        char_hist[ch] = 1

  return word_hist, char_hist

def print_stats(words, word_hist, char_hist):
  # Num words, characters, unique words
  n_chars = 0
  for word in words:
    n_chars += len(word)

  # Needed for median and pN calculations
  sorted_words = sorted(words, key=lambda x: len(x))

  print('%d words, %d characters, %d unique words, %d unique characters' % (len(words), n_chars, 
    len(word_hist), len(char_hist)))
  print('Overall: %.1f avg word length, %d median word length (\'%s\'), %d p90 word length (\'%s\')' 
    % (n_chars/len(words), 
       len(sorted_words[int(len(sorted_words) * 0.5)-1]), 
       sorted_words[int(len(sorted_words) * 0.5)-1],
       len(sorted_words[int(len(sorted_words) * 0.9)-1]), 
       sorted_words[int(len(sorted_words) * 0.9)-1] ))
  
  n_chars = 0
  for word in word_hist.keys():
    n_chars += len(word)

  # NOTE: using 'reverse' so that the sort is consistent with the sort for we use in the other 
  # method for *displaying* the histogram. This way, words of same length will be in the same
  # order in both places, thus making it easier to confirm that we're doing the percentiles correctly.
  sorted_unique_words = sorted(word_hist.keys(), key=lambda x: len(x), reverse=True)
  print('Unique words: %.1f avg word length, %d median word length (\'%s\'), %d p90 word length (\'%s\')'
    % (n_chars/len(word_hist.keys()),
      len(sorted_unique_words[int(len(sorted_unique_words) * 0.5)-1]),
      sorted_unique_words[int(len(sorted_unique_words) * 0.5)-1], 
      len(sorted_unique_words[int(len(sorted_unique_words) * 0.1)-1]), # 0.1 because of reverse sort
      sorted_unique_words[int(len(sorted_unique_words) * 0.1)-1] )) # 0.1 because of reverse sort

  print('') # empty line

def print_histograms(word_hist, char_hist):
  """Print side by side to better use the space: 
        - histogram of word counts sorted by word length
        - histogram of word counts sorted by word count
        - list of unique words in alphabetical order
        - histogram of character frequencies
  """
  words_by_len = sorted(word_hist.keys(), key=lambda x: len(x), reverse=True)
  word_KVs_by_freq = sorted(word_hist.items(), key=lambda x: x[1], reverse=True)
  words_by_alpha = sorted(word_hist.keys())
  char_KVs_by_freq = sorted(char_hist.items(), key=lambda x: x[1], reverse=True)
  
  heading1 = 'Words by length'
  heading2 = 'Words by frequency'
  heading3 = 'Words sorted alphabetically'
  heading4 = 'Character frequencies'
  print(heading1 + ' ' * (COLUMN_WIDTH - len(heading1)) 
      + heading2 + ' ' * (COLUMN_WIDTH - len(heading2)) 
      + heading3 + ' ' * (COLUMN_WIDTH - len(heading3))
      + heading4)
  print('-' * len(heading1) + ' ' * (COLUMN_WIDTH - len(heading1)) 
      + '-' * len(heading2) + ' ' * (COLUMN_WIDTH - len(heading2)) 
      + '-' * len(heading3) + ' ' * (COLUMN_WIDTH - len(heading3)) 
      + '-' * len(heading4))

  for i in range(len(words_by_len)):
    formatted_str1 = '%s %d' % (words_by_len[i], word_hist[words_by_len[i]])
    formatted_str1 = formatted_str1 + ' ' * (COLUMN_WIDTH - len(formatted_str1))
    formatted_str2 = '%s %d' % (word_KVs_by_freq[i][0], word_KVs_by_freq[i][1])
    formatted_str2 = formatted_str2 + ' ' * (COLUMN_WIDTH - len(formatted_str2))
    formatted_str3 = words_by_alpha[i] + ' ' * (COLUMN_WIDTH - len(words_by_alpha[i]))
    formatted_str4 = '%s %d' % (char_KVs_by_freq[i][0], char_KVs_by_freq[i][1]) if i < len(char_KVs_by_freq) else ''
    print(formatted_str1 + formatted_str2 + formatted_str3 + formatted_str4)

  # Print remaining char freqs if unique word count is less than unique character count
  for i in range(len(words_by_len), len(char_KVs_by_freq)):
    print(' ' * 3 * COLUMN_WIDTH + '%s %d' % (char_KVs_by_freq[i][0], char_KVs_by_freq[i][1]))

def print_results(filename, words, word_hist, char_hist):
  print(filename)
  print('-' * len(filename))
  print_stats(words, word_hist, char_hist)
  print_histograms(word_hist, char_hist)

############################## MAIN ##############################
input_filename = get_input_filename()
words = populate_word_list(input_filename)
word_hist, char_hist = create_histograms(words)
print_results(input_filename, words, word_hist, char_hist)
