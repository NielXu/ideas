import * as CryptoJS from 'crypto-js';

class Block {
  // General data about this block
  index: number;
  prevHash: string;
  timestamp: number;
  data: string;
  hash: string;

  constructor(index: number, prevHash: string, timestamp: number,
      data: string, hash: string) {
    this.index = index;
    this.prevHash = prevHash.toString();
    this.timestamp = timestamp;
    this.data = data;
    this.hash = hash;
  }
}

class BlockChain {
  blockchain: Block[];

  constructor() {
    this.blockchain = [this.getGenesisBlock()];
  }

  calcHash(index: number, prevHash: string, timestamp: number, data: string): string {
    return CryptoJS.SHA256(index + prevHash + timestamp + data).toString();
  }

  calcBlockHash(block: Block): string {
    return this.calcHash(block.index, block.prevHash, block.timestamp, block.data).toString();
  }

  getLatestBlock(): Block {
    return this.blockchain[this.blockchain.length-1];
  }

  getGenesisBlock(): Block {
    const timestamp = 1621805758983;
    const message = "Smart Idea";
    return new Block(
      0,
      "0",
      1621805758983,
      message,
      this.calcHash(0, "0", timestamp, message),
    );
  }

  getBlock(data: string): Block {
    const lastBlock = this.getLatestBlock();
    const index = lastBlock.index + 1;
    const timestamp = new Date().getTime();
    const hash = this.calcHash(index, lastBlock.hash, timestamp, data);
    return new Block(index, lastBlock.hash, timestamp, data, hash);
  }

  addBlock(block: Block): { success: boolean, error?: string } {
    const { success, error } = this.isValidBlock(block, this.getLatestBlock());
    if (success) {
      this.blockchain.push(block);
      return { success };
    } else {
      return { success, error };
    }
  }

  isValidBlock(newBlock: Block, prevBlock: Block): { success: boolean, error?: string } {
    if (prevBlock.index + 1 !== newBlock.index) {
      return { success: false, error: "Invalid index" }
    }
    else if (prevBlock.hash !== newBlock.prevHash) {
      return { success: false, error: "Invalid previous block hash" }
    }
    else if (this.calcBlockHash(newBlock) !== newBlock.hash) {
      return {
        success: false,
        error: `Invalid hash, expected: ${this.calcBlockHash(newBlock)}, actual: ${newBlock.hash}`
      }
    }
    return { success: true }
  }

  replaceChain(newChain: Block[]): { success: boolean, error?: string } {
    if (this.isValidChain(newChain) && newChain.length > this.blockchain.length) {
      this.blockchain = newChain;
      return { success: true }
    } else {
      return { success: false, error: "Invalid chain" }
    }
  }

  isValidChain(chain: Block[]): boolean {
    if (JSON.stringify(chain[0]) !== JSON.stringify(this.getGenesisBlock())) {
      return false;
    }
    let tempChain = [chain[0]];
    for (var i = 1; i < chain.length; i++) {
      if (this.isValidBlock(chain[i], chain[i-1])) {
        tempChain.push(chain[i]);
      } else {
        return false;
      }
    }
    return true;
  }
}

export { Block, BlockChain };
