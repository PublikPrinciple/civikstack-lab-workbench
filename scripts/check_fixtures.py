"""Validate starter data shape and references, not capability accuracy."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def validate(root=ROOT):
    load = lambda name: json.loads((root / 'fixtures' / (name + '.json')).read_text())
    sources, programs, requests = load('sources'), load('programs'), load('requests')
    for records in (sources, programs, requests):
        ids = [x['id'] for x in records]
        if len(ids) != len(set(ids)):
            raise ValueError('duplicate IDs')
    source_ids = {x['id'] for x in sources}
    program_ids = {x['id'] for x in programs}
    request_ids = {x['id'] for x in requests}
    for p in programs:
        for field in ('id', 'name', 'age_min', 'age_max', 'hours', 'accommodations', 'availability', 'source_ids'):
            if field not in p:
                raise ValueError('missing program field: ' + field)
        if type(p['age_min']) is not int or type(p['age_max']) is not int or not 0 <= p['age_min'] <= p['age_max']:
            raise ValueError('invalid age range')
        if p['availability'] is not None and type(p['availability']) is not bool:
            raise ValueError('availability must be boolean or null')
        if p['accommodations'] is not None and (not isinstance(p['accommodations'], list) or not all(isinstance(x,str) for x in p['accommodations'])):
            raise ValueError('accommodations must be a string list or null')
        if not p['source_ids'] or not set(p['source_ids']) <= source_ids:
            raise ValueError('unresolved source')
    for req in requests:
        if type(req['age']) is not int or req['age'] < 0 or not isinstance(req['needs'],list):
            raise ValueError('invalid request')
    response = load('response-example')
    if response['request_id'] not in request_ids or not set(response['candidate_program_ids']) <= program_ids or not set(response['evidence_ids']) <= source_ids:
        raise ValueError('unresolved response reference')
    if not response['unknowns'] or not response['next_steps']:
        raise ValueError('missing uncertainty or next step')
    return len(programs)
if __name__ == '__main__':
    print(f'Validated {validate()} synthetic program records; this is not capability evaluation.')
