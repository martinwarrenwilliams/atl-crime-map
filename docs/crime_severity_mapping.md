# Crime Severity Classification System
## Atlanta Crime Data (1997-2024)

---

## Severity Level Definitions

### High Severity (Violent Crimes)
**Definition**: Crimes involving violence or threat of violence against persons, causing or potentially causing serious physical harm or death.

- Homicide
- Rape / Sexual assault  
- Aggravated assault
- Armed robbery (with weapon)

### Medium Severity (Serious Property & Drug Crimes)
**Definition**: Crimes involving significant property loss/damage, breaking and entering, or serious drug offenses.

- Burglary
- Auto theft
- Larceny-theft (large amounts)
- Weapons charges
- Drug trafficking

### Low Severity (Minor Property & Nuisance Crimes)
**Definition**: Minor offenses involving small property loss, public order violations, or non-violent disturbances.

- Simple assault (no weapon, no serious injury)
- Vandalism
- Disorderly conduct
- Trespassing
- Public intoxication  
- Drug possession (personal use amounts)

---

## UCR Code Mappings (1997-2008 Data)

### HIGH SEVERITY

| UCR Code | Description | Notes |
|----------|-------------|-------|
| 110 | Homicide/Willful Killing | All variations including family, non-family, police officer |
| 120 | Negligent Manslaughter | |
| 210 | Rape (all variations) | Gun, other weapon, strongarm |
| 220 | Attempted Rape | All variations |
| 311-347 | Armed Robbery | Includes street, business, residence, bank robberies with weapons |
| 410-440 | Aggravated Assault | When specified as aggravated with gun/knife/weapon |

### MEDIUM SEVERITY

| UCR Code | Description | Notes |
|----------|-------------|-------|
| 511-532 | Burglary | Forced and no-forced entry, residential and non-residential |
| 610-690 | Larceny/Theft | From buildings, vehicles, mail, etc. |
| 710-730 | Auto Theft | Including trucks, vans, buses |

### LOW SEVERITY

| UCR Code | Description | Notes |
|----------|-------------|-------|
| 410-440 | Simple Assault | When specified as simple (no weapon) |
| 610 | Pocket Picking | Minor theft |
| 630 | Shoplifting | When specified |
| 660 | Bicycle Theft | |

---

## NIBRS Code Mappings (2009-2024 Data)

### HIGH SEVERITY

| NIBRS Code | Description | Notes |
|------------|-------------|-------|
| 09A | Murder & Nonnegligent Manslaughter | |
| 11A | Rape | |
| 11B | Sodomy | |
| 11C | Sexual Assault with An Object | |
| 11D | Fondling | Sexual offenses |
| 120, 1201-1299 | Robbery | All robbery variations |
| 13A, 1313-1399 | Aggravated Assault | |
| 100 | Kidnapping/Abduction | |
| 36A | Incest | |
| 36B | Statutory Rape | |
| 64A, 64B | Human Trafficking | Commercial sex acts, involuntary servitude |

### MEDIUM SEVERITY

| NIBRS Code | Description | Notes |
|------------|-------------|-------|
| 200 | Arson | |
| 210 | Extortion/Blackmail | |
| 220, 2202-2206 | Burglary/Breaking & Entering | |
| 240, 2404-2434 | Motor Vehicle Theft | |
| 23D | Theft From Building | |
| 23F | Theft From Motor Vehicle | |
| 23G | Theft of Motor Vehicle Parts | |
| 250 | Counterfeiting/Forgery | |
| 26A-26G | Fraud Offenses | False pretenses, credit card fraud, identity theft, wire fraud |
| 270 | Embezzlement | |
| 280 | Stolen Property Offenses | |
| 23H | All Other Larceny | General theft/larceny |
| 35A | Drug/Narcotic Violations | Trafficking level |
| 520 | Weapon Law Violations | |

### LOW SEVERITY

| NIBRS Code | Description | Notes |
|------------|-------------|-------|
| 13B | Simple Assault | |
| 13C | Intimidation | |
| 23A | Pocket-picking | Minor theft |
| 23B | Purse-snatching | Minor theft |
| 23C | Shoplifting | |
| 23E | Theft From Coin-Operated Machine | Minor property crime |
| 290 | Destruction/Damage/Vandalism | Vandalism |
| 35B | Drug Equipment Violations | Personal use paraphernalia |
| 370 | Pornography/Obscene Material | |
| 39B, 39C | Gambling Violations | |
| 40A, 40B | Prostitution | |
| 510 | Bribery | |
| 720 | Animal Cruelty | |
| 90A | Bad Checks | |
| 90B | Curfew/Loitering/Vagrancy | |
| 90C | Disorderly Conduct | |
| 90D | Driving Under the Influence | |
| 90E | Drunkenness | |
| 90F | Family Offenses, Nonviolent | |
| 90G | Liquor Law Violations | |
| 90H | Peeping Tom | |
| 90J | Trespass of Real Property | |
| 90Z | All Other Offenses | |

---

## Implementation Notes

### Data Processing Guidelines

1. **Code Variations**: Some UCR/NIBRS codes have multiple descriptions across datasets. Use the primary offense type to determine severity.

2. **Mixed Severity Codes**: Some codes (e.g., UCR 410-440) can represent both aggravated assault (HIGH) and simple assault (LOW). Check the description field for keywords:
   - If contains "AGGR" or weapon type → HIGH
   - If contains "SIMPLE" → LOW

3. **Default Classifications**: When ambiguous, default to the higher severity level for public safety prioritization.

4. **Special Cases**:
   - Robbery codes (UCR 311-347, NIBRS 120 series): Always HIGH due to violence/threat
   - Larceny codes: Generally MEDIUM unless specified as minor (shoplifting, pocket-picking)
   - Drug offenses: Distinguish between trafficking (MEDIUM) and possession (LOW)

### Python Implementation Example

```python
def get_severity_level(code, description):
    """
    Maps crime codes to severity levels.
    
    Args:
        code: UCR or NIBRS code
        description: Crime description text
        
    Returns:
        'HIGH', 'MEDIUM', or 'LOW'
    """
    
    # High severity codes
    high_codes = {
        # UCR codes
        '110', '120', '210', '220',
        # NIBRS codes  
        '09A', '11A', '11B', '11C', '11D', '100',
        '36A', '36B', '64A', '64B'
    }
    
    # Check robbery codes (UCR 3xx series, NIBRS 12xx series)
    if code.startswith('3') and 311 <= int(code[:3]) <= 347:
        return 'HIGH'
    if code.startswith('12'):
        return 'HIGH'
        
    # Check assault codes for type
    if code.startswith('4') or code == '13A' or code.startswith('13'):
        if 'AGGR' in description.upper() or 'GUN' in description.upper():
            return 'HIGH'
        elif 'SIMPLE' in description.upper():
            return 'LOW'
            
    # Continue with other mappings...
    if code in high_codes:
        return 'HIGH'
    
    # Similar logic for MEDIUM and LOW codes
    
    return 'MEDIUM'  # Default for unknown codes
```

---

## Data Sources

- **UCR Codes**: Crime_Data_1997_2008 (54 unique codes, 206 code-description pairs)
- **NIBRS Codes 2009-2020**: 2009_2020CrimeData (105 unique codes)
- **NIBRS Codes 2020+**: AxonCrimeData_Export (57 unique codes)
- **Total Unique Crime Codes**: 203 codes across all datasets

---

*Last Updated: December 2024*
*Document Version: 1.0*