#include <stdlib.h>
#include <stdio.h>

typedef struct {
	int day;
	int month;
	int year;
} date;

struct _date_interval {
	date *start_date;
	date *end_date;
};

typedef struct _date_interval date_interval;

struct _interval_list {
	date_interval *val;
	struct _interval_list *next;
};

typedef struct _interval_list interval_list;

int date_compare(date *d1, date *d2) {
	if (d1->year > d2->year) {
		return 1;
	} else if (d1->year < d2->year) {
		return -1;
	}
	if (d1->month > d2->month) {
		return 1;
	} else if (d1->month < d2->month) {
		return -1;
	} else if (d1->day > d2->day) {/* year, month equal when enter this if */
		return 1;
	} else if (d1->day < d2->day) {
		return -1;
	} else {
		return 0;/* equal */
	}
}

int merge_interval(interval_list *list, date_interval *new_interval) {
	interval_list *current_interval;
	interval_list *new_list;
	current_interval = list;

	printf("entering\n %d", current_interval->val->start_date->day);
	int i = 0;

	while (current_interval) {
		printf("in hilw: %d\n", current_interval->val->start_date->day);
		new_list = malloc(sizeof(interval_list));

		int result;
		result = date_compare(current_interval->val->start_date, new_interval->start_date);
		if (result == -1) {
			printf("Less\n");
		} else if (result == 0) {
			printf("Equal\n");
		} else {
			printf("Bigger\n");
		}

		current_interval = current_interval->next;
		i++;
	}

	return 0;
}

date_interval *
create_date_interval(int y1, int m1, int d1, int y2, int m2, int d2) {
	date_interval *one = malloc(sizeof(date_interval));
	date *s = malloc(sizeof(date));
	date *e = malloc(sizeof(date));
	s->year = y1;
	s->month = m1;
	s->day = d1;
	e->year = y2;
	e->month = m2;
	e->day = d2;
	one->start_date = s;
	one->end_date = e;
	return one;
}

int main() {
	printf("running main\n");
	interval_list *list = malloc(sizeof(interval_list));
	interval_list *head;
	head = NULL;
	list->val = create_date_interval(2013, 1, 20, 2013, 3, 20);
	list->next = head;
	head = list;
	list = malloc(sizeof(interval_list));
	list->val = create_date_interval(2013, 4, 22, 2013, 5, 20);
	list->next = head;
	head = list;
	list = malloc(sizeof(interval_list));
	list->val = create_date_interval(2013, 5, 21, 2013, 6, 20);
	list->next = head;
	head = list;
	list = head;

	date_interval *new_int = malloc(sizeof(date_interval));

	date *s = malloc(sizeof(date));
	date *e = malloc(sizeof(date));
	s->year = 2013;
	s->month = 5;
	s->day = 10;
	e->year = 2013;
	e->month = 7;
	e->day = 10;
	new_int->start_date = s;
	new_int->end_date = e;

	merge_interval(list, new_int);

	free(new_int->start_date);
	free(new_int->end_date);
	free(new_int);
	interval_list *current;
	while(list) {
		current = list;
		list = list->next;
		free(current->val->end_date);
		free(current->val->start_date);
		free(current->val);
		free(current);
	}
	return 0;
}

