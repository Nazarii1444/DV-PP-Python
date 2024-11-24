from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class CustomsDeclaration:
    vehicle: str
    license_plate: str
    owner: str
    date: str
    origin: Tuple[str, str]
    destination: Tuple[str, str]
    goods: List[Tuple[str, float]]
    transport_agreement: bool
    other_info: Optional[str] = None

class Queue:
    """Queue class for modeling customs border control."""

    def __init__(self, name: str):
        self.queue = []
        self.name = name

    def add(self, item: CustomsDeclaration):
        """Adds an item to the queue."""
        self.queue.append(item)
        message = f"[{self.name}] Added: {item.vehicle} ({item.license_plate})"
        return message

    def remove(self):
        """Removes an item from the queue (after inspection)."""
        if self.queue:
            item = self.queue.pop(0)
            message = f"[{self.name}] Vehicle {item.vehicle} ({item.license_plate}) passed inspection."
            return message
        else:
            message = f"[{self.name}] The queue is empty."
            return message

    def transfer_to(self, other_queue, license_plate: str):
        """Transfers a vehicle from one queue to another."""
        for i, item in enumerate(self.queue):
            if item.license_plate == license_plate:
                other_queue.add(item)
                self.queue.pop(i)
                message = f"Transferred vehicle {license_plate} to {other_queue.name}."
                return message
        message = f"Vehicle {license_plate} not found in {self.name}."
        return message

    def remove_by_license(self, license_plate: str):
        """Removes a vehicle from the queue (no border crossing permission)."""
        for i, item in enumerate(self.queue):
            if item.license_plate == license_plate:
                removed = self.queue.pop(i)
                message = f"[{self.name}] Removed vehicle by license {removed.vehicle} ({removed.license_plate})."
                return message
        message = f"Vehicle {license_plate} not found in {self.name}."
        return message

    def filter_by_goods(self, good_name: str):
        """Returns a list of vehicles carrying a specified good."""
        return [item for item in self.queue if any(good[0] == good_name for good in item.goods)]

    def max_value_item(self):
        """Finds the vehicle with the most valuable goods."""
        if not self.queue:
            return None
        return max(self.queue, key=lambda x: x.goods[0][1])

    def summary_of_goods(self):
        """Returns a summary of goods and their total value."""
        goods_summary = {}
        for item in self.queue:
            for good, value in item.goods:
                if good in goods_summary:
                    goods_summary[good] += value
                else:
                    goods_summary[good] = value
        return goods_summary


    def filter_by_destination(self, city: str):
        """Finds all vehicles heading to the specified city."""
        return [item for item in self.queue if item.destination[1] == city]


    def check_for_dangerous_goods(self):
        """Check if any vehicle is transporting narcotics or explosives."""
        dangerous_goods = ["Narcotics", "Explosives"]
        for item in self.queue:
            for good, _ in item.goods:
                if good in dangerous_goods:
                    message = f"[{self.name}] Dangerous good found: {good} in {item.vehicle} ({item.license_plate})"
                    return message
        return f"No dangerous goods found in {self.name}."

    def filter_by_value_above(self, min_value: float):
        """Returns a list of vehicles carrying goods above a certain value."""
        return [item.vehicle+f" ({item.license_plate})" for item in self.queue if any(good[1] > min_value for good in item.goods)]

    def transfer_all_to_city(self, other_queue, city: str):
        """Transfers all vehicles heading to a specific city to another queue."""
        transferred = [item for item in self.queue if item.destination[1] == city]
        for item in transferred:
            self.queue.remove(item)
            other_queue.add(item)
        message = f"Transferred all vehicles to {city} to {other_queue.name}."
        return message

    def validate_transport_agreements(self):
        """Ensure all vehicles in the queue have valid transport agreements."""
        for item in self.queue:
            if not item.transport_agreement:
                message = f"[{self.name}] Vehicle {item.vehicle} ({item.license_plate}) has no transport agreement."
                return message
        return f"All vehicles in {self.name} have valid agreements."

    def print_queue(self):
        """Prints the current state of the queue."""
        if not self.queue:
            message = f"[{self.name}] The queue is empty."
        else:
            message = f"[{self.name}] Current queue:"
            for i, item in enumerate(self.queue):
                message += f"\n{i + 1}. {item.vehicle} ({item.license_plate}) - {item.destination}"
        return message


def write_to_protocol(message: str):
    """Writes a message to the protocol file."""
    with open("protocol.txt", "a") as f:
        f.write(message + "\n")


def run_scenario():
    """Run a scenario demonstrating various operations."""
    # Create queues
    general_queue = Queue("General Queue")
    green_lane_queue = Queue("Green Lane")

    # Manually create 15 declarations
    declarations = [
        CustomsDeclaration("Volvo", "D1093AH", "Green Day Co", "2024-10-10",
                           ("Poland", "Warsaw"), ("Ukraine", "Odessa"), [("Textile", 5000.0)], True),
        CustomsDeclaration("Scania", "B2039BV", "Fast Trucking", "2024-10-11",
                           ("Germany", "Berlin"), ("Ukraine", "Lviv"), [("Electronics", 12000.0)], True),
        CustomsDeclaration("MAN", "A9843CT", "TransRoad", "2024-10-12",
                           ("Hungary", "Budapest"), ("Ukraine", "Odessa"), [("Furniture", 8000.0)], False),
        CustomsDeclaration("Mercedes", "E1024EX", "CargoLine", "2024-10-13",
                           ("Poland", "Krakow"), ("Ukraine", "Kyiv"), [("Clothing", 3000.0)], True),
        CustomsDeclaration("DAF", "T5647AA", "Global Trans", "2024-10-14",
                           ("Slovakia", "Bratislava"), ("Ukraine", "Odessa"), [("Machinery", 15000.0)], True),
        CustomsDeclaration("Iveco", "G2034BC", "EuroCargo", "2024-10-15",
                           ("Czech Republic", "Prague"), ("Ukraine", "Lviv"), [("Food", 2000.0)], True),
        CustomsDeclaration("Volvo", "Z8390AD", "Green Day Co", "2024-10-16",
                           ("Germany", "Munich"), ("Ukraine", "Odessa"), [("Textile", 6000.0)], False),
        CustomsDeclaration("Scania", "H5648XY", "Fast Trucking", "2024-10-17",
                           ("Austria", "Vienna"), ("Ukraine", "Kyiv"), [("Electronics", 18000.0)], True),
        CustomsDeclaration("MAN", "V2039AB", "TransRoad", "2024-10-18",
                           ("Poland", "Warsaw"), ("Ukraine", "Odessa"), [("Furniture", 7000.0)], True),
        CustomsDeclaration("Mercedes", "M9842KW", "CargoLine", "2024-10-19",
                           ("Germany", "Berlin"), ("Ukraine", "Lviv"), [("Clothing", 4000.0)], False),
        CustomsDeclaration("DAF", "X5643YZ", "Global Trans", "2024-10-20",
                           ("Hungary", "Budapest"), ("Ukraine", "Odessa"), [("Machinery", 14000.0)], True),
        CustomsDeclaration("Iveco", "Q2038AC", "EuroCargo", "2024-10-21",
                           ("Austria", "Vienna"), ("Ukraine", "Kyiv"), [("Food", 3500.0)], False),
        CustomsDeclaration("Volvo", "L8395CD", "Green Day Co", "2024-10-22",
                           ("Poland", "Krakow"), ("Ukraine", "Odessa"), [("Textile", 5500.0)], True),
        CustomsDeclaration("Scania", "P5647LM", "Fast Trucking", "2024-10-23",
                           ("Slovakia", "Bratislava"), ("Ukraine", "Lviv"), [("Electronics", 16000.0)], True),
        CustomsDeclaration("MAN", "T2039XY", "TransRoad", "2024-10-24",
                           ("Czech Republic", "Prague"), ("Ukraine", "Odessa"), [("Furniture", 9000.0)], True)
    ]

    # Add declarations to the general queue
    for decl in declarations:
        message = general_queue.add(decl)
        write_to_protocol(message)

    # Transfer vehicles between queues
    message = general_queue.transfer_to(green_lane_queue, "B2039BV")
    write_to_protocol(message)

    # Remove vehicle from queue (no permission)
    message = general_queue.remove_by_license("A9843CT")
    write_to_protocol(message)

    # Find vehicles carrying a specific good
    textile_vehicles = general_queue.filter_by_goods("Textile")
    write_to_protocol("\nVehicles carrying Textile:")
    for item in textile_vehicles:
        message = f"  {item.vehicle} ({item.license_plate})"
        write_to_protocol(message)

    # Find the vehicle with the most valuable goods
    most_valuable = general_queue.max_value_item()
    if most_valuable:
        message = f"\nVehicle with the most valuable goods: {most_valuable.vehicle} ({most_valuable.license_plate})"
        write_to_protocol(message)

    # Get a summary of all goods and their total value
    goods_summary = general_queue.summary_of_goods()
    write_to_protocol("\nSummary of goods and their total value:")
    for good, value in goods_summary.items():
        message = f"  {good}: {value} USD"
        write_to_protocol(message)

    # Find vehicles heading to Odessa and log to protocol
    to_odesa = general_queue.filter_by_destination("Odessa")
    write_to_protocol("\nVehicles heading to Odessa:")

    for item in to_odesa:
        message = f"  {item.vehicle} ({item.license_plate})"

        write_to_protocol(message)

    # Check for dangerous goods
    message = green_lane_queue.check_for_dangerous_goods()
    write_to_protocol(message)

    # Check transport agreements
    message = general_queue.validate_transport_agreements()
    write_to_protocol(message)

    # Vehicles with goods above
    message = general_queue.filter_by_value_above(15000)
    write_to_protocol(f"\nVehicles with goods above 15000 USD:")
    for item in message:
        write_to_protocol(f" {item}")
    # Transfer all to
    message = general_queue.transfer_all_to_city(green_lane_queue, "Lviv")
    write_to_protocol("\n"+message)

    # passed inspection
    message = general_queue.remove()
    write_to_protocol("\n"+message)
    message = green_lane_queue.remove()
    write_to_protocol(message)

    # Print the final state of both queues
    message = general_queue.print_queue()
    write_to_protocol("\n"+message)
    message = green_lane_queue.print_queue()
    write_to_protocol(message)



if __name__ == "__main__":

    with open("protocol.txt", "w") as f:
        f.write("Customs Control Protocol:\n")

    run_scenario()