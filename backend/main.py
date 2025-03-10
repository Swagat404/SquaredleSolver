import nltk
from nltk.corpus import words
import os

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

def load_word_list():
    #nltk.download("words")
    word_list = set(word.lower() for word in words.words() if len(word) >= 4)
    trie = Trie()
    for word in word_list:
        trie.insert(word)
    return trie

def load_local_crossword_words(repo_path="dictionary"):
    """
    Load words from the local cloned crossword-dataset repository
    """
    # Path to the core word list
    core_path = os.path.join(repo_path, "popular.txt")
    
    # Read and process the local file
    words = set()
    try:
        with open(core_path, 'r') as f:
            for line in f:
                entry = line.strip().lower()
                # Filter out phrases with spaces and non-alphabetic entries
                if ' ' in entry or not entry.isalpha():
                    continue
                words.add(entry)
    except FileNotFoundError:
        raise RuntimeError(f"core.txt not found at {core_path}")

    # Build trie
    trie = Trie()
    for word in words:
        if len(word) >= 4:  # Same as original filter
            trie.insert(word)
    return trie



def find_words(grid, trie, required_counts):
    rows, cols = len(grid), len(grid[0])
    found_words = {length: set() for length in required_counts}
    
    def backtrack(r, c, path, word):
        if len(word) in required_counts and word not in found_words[len(word)] and trie.search(word):
            found_words[len(word)].add(word)
        
        if len(word) >= max(required_counts):
            return
        
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in path:
                new_word = word + grid[nr][nc]
                if trie.starts_with(new_word):
                    backtrack(nr, nc, path | {(nr, nc)}, new_word)
    
    for r in range(rows):
        for c in range(cols):
            backtrack(r, c, {(r, c)}, grid[r][c])
    
    return {k: list(v)[:required_counts[k]] for k, v in found_words.items()}  # Return only required count of words

# Example Usage
grid = [
    ["b", "n", "o", "k"],
    ["t", "i", "n", "v"],
    ["s", "g", "i", "b"],
    ["h", "e", "l", "a"]
]

required_counts = {
    4: 320,  # Examples: "acre", "aero", "alma", "aloe", "balm", etc.
    5: 100,  # Examples: "cabal", "clamp", "glace", "lacer", "macro", etc.
    6: 30,   # Examples: "boreal", "palace", "placer"
    7: 10 ,   # Example: "acerola"
    8:100,
    9:100,

}

trie = load_local_crossword_words()
found_words = find_words(grid, trie, required_counts)
print(found_words)


