from socscraper import scrape
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('term', type=int)
    parser.add_argument('year', type=int)
    parser.add_argument('campus', type=str)

    args = parser.parse_args()

    output_filename = '{}-{}-{}.json'.format(args.term, args.year, args.campus)

    fieldsMap = {
        'title': 'name',
        'offeringUnitCode': 'offering_unit',
        'subject': 'subject',
        'courseNumber': 'course_number',
    }

    scrape(args.year, args.term, args.campus, output_filename, fieldsMap)
