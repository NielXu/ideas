def get_parent_hash(block):
    return block[0]


def get_transactions(block):
    return block[1]


def get_hash_self(block):
    return block[2]


def create_block(transactions, parent_hash):
    hash_itself = hash((transactions, parent_hash))
    return (parent_hash, transactions, hash_itself)


def create_genesis_block(transactions):
    return create_block(transactions, 0)


genesis_block = create_genesis_block("X paid $20 to Y")
genesis_block_hash = get_hash_self(genesis_block)
print("genesis_block_hash:", genesis_block_hash)

block_1 = create_block("Y paid $20 to Z, X paid $10 to P", genesis_block_hash)
block_1_hash = get_hash_self(block_1)
print("block_1_hash:", block_1_hash)
