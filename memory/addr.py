"""
Calculations and algorithms related to memory management.
Calculate single paging:
    Given:
        Virtual Address(VA) = x
        Page Size = y
    Formula:
        Offset = log2(y) bits
        Page Number = (x - Offset) bits
        Number of Page = 2^(Page Number)
    Example:
        VA = 16 bits, Page Size = 4K(4096 bytes)
        Offset = log2(4096) = 12 bits
        Page Number = 16 - 12 = 4 bits
        Number of Page = 2^4 = 16
    Graph:
        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  =>  16 bits in total
        |_____| |_____________________|
      Page Number       Offset
         4 bits         12 bits
"""
from math import log2

def addr_translate(vaddr, page_table, page_size=4096, hexstr=False):
    """
    Address translation. Translate the given virtual
    address to physical address, return the result
    in format `(paddr, page, offset)`.

    `vaddr`: The virtual address in hexadecimal format

    `page_table`: A page table in a dict with format:
        {page#: frame#}
    
    `page_size=4096`: The page size, default is 4K

    `hexstr=False`: Set it to True and the return paddr will
    be a hex string instead of integer
    """
    page = vaddr >> 12
    if page not in page_table:
        raise "Page not found in page table"
    frame = page_table[page]
    offset = vaddr % page_size
    paddr = frame * page_size + offset
    return (paddr if not hexstr else hex(paddr), page, offset)


def page_alloc(address_size, page_size=4096):
    """
    Calculate the page number size and offset size given
    the address_size and page_size. Return the result in format
    `(page_number_size, offset_size)`

    `Example`: address_size = 16bits, page_size = 4K(4096 bytes)
    offset_size = 12(2^12 = 4096), page_number_size = 4(16-12 = 4).
    It means the first 4 bits will represent the page number and
    the last 12 bits will represent the offset.

    `address_size`: Specify the number of bits required for
    the memory address

    `page_size=4096`: Specify the total amount of memory can be
    allocated,in bytes. Default is 4096 bytes, i.e. 4K
    """
    offset_size = log2(page_size)
    page_number_size = address_size - offset_size
    return (page_number_size, offset_size)


def belady_replacement(addr_list, page):
    """
    Using belady replacement to reduce the fault rate, print
    every step on the console. Return the result in format:
    `(evicted rate, fault rate)`

    `addr_list`: A list of addresses, usually use integers to
    represent the addresses.

    `page`: The number of pages available
    """
    slots = []
    index = 0
    evicted_count = 0
    fault_count = 0
    while index < len(addr_list):
        enter = addr_list[index]
        print('Slots:', slots, 'Entering', enter, end=' ')
        if enter in slots:
            index += 1
            print('Existed')
            continue
        # Require to evict a page to make room
        if len(slots) >= page:
            candidate = None
            for j in slots:
                cpIndex = index
                dist = -1
                # Move forward to find the next entry of this page
                while cpIndex < len(addr_list):
                    # If found, record the distance
                    if j == addr_list[cpIndex]:
                        dist = cpIndex - index
                        break
                    cpIndex += 1
                if dist == -1:
                    candidate = (dist, j)
                else:
                    if not candidate or candidate[0] < dist:
                        candidate = (dist, j)
            evicted = slots.index(candidate[1])
            slots[evicted] = enter
            evicted_count += 1
            fault_count += 1
            print('Evicted', candidate[1], 'Result', slots)
        # Enough room to add it to the slot
        else:
            slots.append(enter)
            fault_count += 1
            print('Enough', 'Result', slots)
        index += 1
    return (evicted_count/len(addr_list), fault_count/len(addr_list))


print(addr_translate(0x3468, {3: 7}, hexstr=True))
print(page_alloc(32))
print(belady_replacement([2,3,2,1,5,4,5,3,5,3,2], 3))