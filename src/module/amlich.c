#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int jd_from_date(int dd, int mm, int yyyy) {
	int a, y, m, jd;
	a = (int) ((14 - mm) / 12);
	y = yyyy + 4800 - a;
	m = mm + 12 * a - 3;
	jd = dd + (int) ((153 * m + 2) / 5) + 365 * y + (int) (y / 4)
			- (int) (y / 100) + (int) (y / 400) - 32045;
	if (jd < 2299161) {
		jd = dd + (int) ((153 * m + 2) / 5) + 365 * y + (int) (y / 4) - 32083;
	}
	return jd;
}

int * jd_to_date(int jd) {
	int a, b, c, d, e, m, day, month, year;
	int * date = (int *) malloc(3 * sizeof(int));
	if (jd > 2299160) { // After 5/10/1582, Gregorian calendar
		a = jd + 32044;
		b = (int) ((4 * a + 3) / 146097);
		c = a - (int) ((b * 146097) / 4);
	} else {
		b = 0;
		c = jd + 32082;
	}
	d = (int) ((4 * c + 3) / 1461);
	e = c - (int) ((1461 * d) / 4);
	m = (int) ((5 * e + 2) / 153);
	day = e - (int) ((153 * m + 2) / 5) + 1;
	month = m + 3 - 12 * (int) (m / 10);
	year = b * 100 + d - 4800 + (int) (m / 10);
	date[0] = day;
	date[1] = month;
	date[2] = year;

	return date;
}

double newmoon(int k) {
	double T, T2, T3, dr, Jd1, M, Mpr, F, C1, deltat, JdNew;
	T = k / 1236.85; // Time in Julian centuries from 1900 January 0.5
	T2 = T * T;
	T3 = T2 * T;
	dr = M_PI / 180;
	Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3;
	Jd1 = Jd1 + 0.00033 * sin((166.56 + 132.87 * T - 0.009173 * T2) * dr); // Mean new moon
	M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3; // Sun's mean anomaly
	Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3; // Moon's mean anomaly
	F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3; // Moon's argument of latitude
	C1 = (0.1734 - 0.000393 * T) * sin(M * dr) + 0.0021 * sin(2 * dr * M);
	C1 = C1 - 0.4068 * sin(Mpr * dr) + 0.0161 * sin(dr * 2 * Mpr);
	C1 = C1 - 0.0004 * sin(dr * 3 * Mpr);
	C1 = C1 + 0.0104 * sin(dr * 2 * F) - 0.0051 * sin(dr * (M + Mpr));
	C1 = C1 - 0.0074 * sin(dr * (M - Mpr)) + 0.0004 * sin(dr * (2 * F + M));
	C1 = C1 - 0.0004 * sin(dr * (2 * F - M)) - 0.0006 * sin(dr * (2 * F + Mpr));
	C1 = C1 + 0.0010 * sin(dr * (2 * F - Mpr))
			+ 0.0005 * sin(dr * (2 * Mpr + M));
	if (T < -11) {
		deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3
				- 0.000000081 * T * T3;
	} else {
		deltat = -0.000278 + 0.000265 * T + 0.000262 * T2;
	};
	JdNew = Jd1 + C1 - deltat;
	return JdNew;
}

double sun_longitude(double jdn) {
	double T, T2, dr, M, L0, DL, L;
	T = (jdn - 2451545.0) / 36525; // Time in Julian centuries from 2000-01-01 12:00:00 GMT
	T2 = T * T;
	dr = M_PI / 180; // degree to radian
	M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2; // mean anomaly, degree
	L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2; // mean longitude, degree
	DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * sin(dr * M);
	DL = DL + (0.019993 - 0.000101 * T) * sin(dr * 2 * M)
			+ 0.000290 * sin(dr * 3 * M);
	L = L0 + DL; // true longitude, degree
	L = L * dr;
	L = L - M_PI * 2 * ((int) (L / (M_PI * 2))); // Normalize to (0, 2*PI)
	return L;
}

int get_sun_longitude(int jd, int time_zone) {
	return (int) (sun_longitude(jd - 0.5 - time_zone / 24) / M_PI * 6);
}

int get_newmoon_day(int k, int time_zone) {
	return (int) (newmoon(k) + 0.5 + time_zone / 24);
}

int get_lunar_month11(int yyyy, int time_zone) {
	int k, off, nm, sun_long;
	//off = jdFromDate(31, 12, yy) - 2415021.076998695;
	off = jd_from_date(31, 12, yyyy) - 2415021;
	k = (int) (off / 29.530588853);
	nm = get_newmoon_day(k, time_zone);
	sun_long = get_sun_longitude(nm, time_zone); // sun longitude at local midnight
	if (sun_long >= 9) {
		nm = get_newmoon_day(k - 1, time_zone);
	}
	return nm;
}

int get_leap_month_offset(int a11, int time_zone) {
	int k, last, arc, i;
	k = (int) ((a11 - 2415021.076998695) / 29.530588853 + 0.5);
	last = 0;
	i = 1; // We start with the month following lunar month 11
	arc = get_sun_longitude(get_newmoon_day(k + i, time_zone), time_zone);
	do {
		last = arc;
		i++;
		arc = get_sun_longitude(get_newmoon_day(k + i, time_zone), time_zone);
	} while (arc != last && i < 14);

	return i - 1;
}

int * solar2lunar(int dd, int mm, int yyyy, int time_zone) {
	int k, dayNumber, monthStart, a11, b11, lunarDay, lunarMonth, lunar_year,
			lunarLeap, diff, leapMonthDiff;

	dayNumber = jd_from_date(dd, mm, yyyy);

	k = (int) ((dayNumber - 2415021.076998695) / 29.530588853);
	monthStart = get_newmoon_day(k + 1, time_zone);
	if (monthStart > dayNumber) {
		monthStart = get_newmoon_day(k, time_zone);
	}
	//alert(dayNumber+" -> "+monthStart);
	a11 = get_lunar_month11(yyyy, time_zone);
	b11 = a11;
	if (a11 >= monthStart) {
		lunar_year = yyyy;
		a11 = get_lunar_month11(yyyy - 1, time_zone);
	} else {
		lunar_year = yyyy + 1;
		b11 = get_lunar_month11(yyyy + 1, time_zone);
	}
	lunarDay = dayNumber - monthStart + 1;
	diff = (int) ((monthStart - a11) / 29);
	lunarLeap = 0;
	lunarMonth = diff + 11;
	if (b11 - a11 > 365) {
		leapMonthDiff = get_leap_month_offset(a11, time_zone);
		if (diff >= leapMonthDiff) {
			lunarMonth = diff + 10;
			if (diff == leapMonthDiff) {
				lunarLeap = 1;
			}
		}
	}
	if (lunarMonth > 12) {
		lunarMonth = lunarMonth - 12;
	}
	if (lunarMonth >= 11 && diff < 4) {
		lunar_year -= 1;
	}
	int * res;
	res = (int *)malloc(4 * sizeof(int));
	res[0] = lunarDay;
	res[1] = lunarMonth;
	res[2] = lunar_year;
	res[3] = lunarLeap;
	return res;
}

int * lunar2solar(int lunar_day, int lunar_month, int lunar_year,
		int lunar_leap, int time_zone) {
	int k, a11, b11, off, leapOff, leapMonth, monthStart;
	int *res;
	res = (int *)malloc(3 * sizeof(int));

	if (lunar_month < 11) {
		a11 = get_lunar_month11(lunar_year - 1, time_zone);
		b11 = get_lunar_month11(lunar_year, time_zone);
	} else {
		a11 = get_lunar_month11(lunar_year, time_zone);
		b11 = get_lunar_month11(lunar_year + 1, time_zone);
	}
	k = (int) (0.5 + (a11 - 2415021.076998695) / 29.530588853);
	off = lunar_month - 11;
	if (off < 0) {
		off += 12;
	}
	if (b11 - a11 > 365) {
		leapOff = get_leap_month_offset(a11, time_zone);
		leapMonth = leapOff - 2;
		if (leapMonth < 0) {
			leapMonth += 12;
		}
		if (lunar_leap != 0 && lunar_month != lunar_leap) {
			res[0] = 0;
			res[1] = 0;
			res[2] = 0;
			return res;
		} else if (lunar_leap != 0 || off >= leapOff) {
			off += 1;
		}
	}
	monthStart = get_newmoon_day(k + off, time_zone);
	res = jd_to_date(monthStart + lunar_day - 1);

	return res;
}
/*
int main() {
	int dd, mm, yyyy, time_zone;
	int * date;
	dd = 10;
	mm = 2;
	yyyy = 2013;
	time_zone = 7;
	date = solar2lunar(dd, mm, yyyy, time_zone);
	printf("%i", date[2]);
	return 0;
}*/


