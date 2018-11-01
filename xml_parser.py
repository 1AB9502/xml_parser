from xml.etree import ElementTree


def get_winning_bid_parent():
    root = ElementTree.parse('targets.xml')
    bid_data = root.findall('.//*[@type="listings"]/auctions/')

    for bid in bid_data:
        for tag in bid:
            if tag.tag == 'won' and tag.text == '1':
                return bid
    return None


def build_winning_data_dict(bid_win_data):
    elements=  {}
    selected_bid_elements = ['listing', 'start_date', 'price']
    # transform bid_elements before sending the object to the template
    bid_elements = {
        'listing': 'Listing',
        'target': 'Start Date',
        'price': ['Winning Price', lambda x: 1000 * float(x)]
    }

    # loop over the winning bid elements to construct a dictionary
    for bid in bid_win_data:
        if bid.tag in selected_bid_elements:
            name = bid_elements[bid.tag]
            value = bid.text
            # price element is a list with 2 elements
            if isinstance(name, list):
                value = name[1](value)
                name = name[0]
            elements[name] = value

    return elements

def get_winning_bid_data():
    bid_win_location = get_winning_bid_parent()
    if bid_win_location is not None:
        return  build_winning_data_dict(bid_win_location)
    else:
        return None

print(get_winning_bid_data())


