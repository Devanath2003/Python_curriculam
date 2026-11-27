from .exceptions import MalFormedLogError

def parse_log_line(raw_line:str) -> tuple[str, str, str, int, float] :
    
    #List comprehension to split each line into corresponding items
    record = [part.strip() for part in raw_line.split("|")]
    
    #checking all items present else raising the custom exception
    if len(record) != 5:
        raise MalFormedLogError(f"Expected 5 fields ; Got {len(record)}parts.")

    # unpakcing contents in the list (yes, we can unpack both list and tuple)
    timestamp, method, endpoint, raw_status, raw_latency = record
    

    # Error handling while converting datatype also raising our custom exception
    try:
        raw_status = int(raw_status)
        raw_latency = float(raw_latency)

    except ValueError:
        
        raise MalFormedLogError("Invalid Numeric status or latency")
        
    
    return (timestamp,method.upper(), endpoint, raw_status, raw_latency)


def parse_logs(raw_lines : list[str]) -> tuple[list[tuple[str, str, str, int, float]],int] :
    
    valid_records = []
    corrupted_count = 0

    for line in raw_lines:
        try:
            log = parse_log_line(line)
            

        except MalFormedLogError:
            corrupted_count += 1
        else:
            
            valid_records.append(log)

    return (valid_records, corrupted_count)




    

