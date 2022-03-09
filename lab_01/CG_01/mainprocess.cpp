#include "mainwindow.h"
#include "ui_mainwindow.h"

//Поиск треугольника
double process(cords_t array[SIZE], int n, cords_t answer[ANS]) {
  long i, j, k;
  double a, b, c;
  double tempsdiff, minsdiff = -1;

  for (i = 0; i < n - 2; i++)
    for (j = i + 1; j < n - 1; j++)
      for (k = j + 1; k < n; k++) {
        a = length(array[i].xc, array[i].yc, array[j].xc, array[j].yc);
        b = length(array[j].xc, array[j].yc, array[k].xc, array[k].yc);
        c = length(array[k].xc, array[k].yc, array[i].xc, array[i].yc);
        tempsdiff = difference(a, b, c);
        if ((a < b + c) && (b < a + c) && (c < a + b)) {
          if ((tempsdiff < minsdiff) || (minsdiff == -1)) {
            minsdiff = tempsdiff;
            answer[0].index = array[i].index;
            answer[0].xc = array[i].xc;
            answer[0].yc = array[i].yc;
            answer[1].index = array[j].index;
            answer[1].xc = array[j].xc;
            answer[1].yc = array[j].yc;
            answer[2].index = array[k].index;
            answer[2].xc = array[k].xc;
            answer[2].yc = array[k].yc;
          }
        } else
          continue;
      }
  return minsdiff;
}

//Нахождение параметров описанной окружности
void outside(cords_t answer[ANS], center_t *outcenter) {
  double a = length(answer[0].xc, answer[0].yc, answer[1].xc, answer[1].yc);
  double b = length(answer[1].xc, answer[1].yc, answer[2].xc, answer[2].yc);
  double c = length(answer[2].xc, answer[2].yc, answer[0].xc, answer[0].yc);
  double p = (a + b + c) / 2;
  double d = 2 * (answer[0].xc * (answer[1].yc - answer[2].yc) +
                  answer[1].xc * (answer[2].yc - answer[0].yc) +
                  answer[2].xc * (answer[0].yc - answer[1].yc));
  outcenter->rad =
      a * b * c / (sqrt(2 * p * (b + c - a) * (a + c - b) * (a + b - c)));
  outcenter->xc =
      (((answer[0].xc) * (answer[0].xc) + (answer[0].yc) * (answer[0].yc)) *
           (answer[1].yc - answer[2].yc) +
       ((answer[1].xc) * (answer[1].xc) + (answer[1].yc) * (answer[1].yc)) *
           (answer[2].yc - answer[0].yc) +
       ((answer[2].xc) * (answer[2].xc) + (answer[2].yc) * (answer[2].yc)) *
           (answer[0].yc - answer[1].yc));
  outcenter->xc /= d;
  outcenter->yc =
      (((answer[0].xc) * (answer[0].xc) + (answer[0].yc) * (answer[0].yc)) *
           (answer[2].xc - answer[1].xc) +
       ((answer[1].xc) * (answer[1].xc) + (answer[1].yc) * (answer[1].yc)) *
           (answer[0].xc - answer[2].xc) +
       ((answer[2].xc) * (answer[2].xc) + (answer[2].yc) * (answer[2].yc)) *
           (answer[1].xc - answer[0].xc));
  outcenter->yc /= d;
}

//Вычисление длины стороны треугольника по координатам её концов
double length(double x1, double y1, double x2, double y2) {
  return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
}

//Подсчет разности площадей треугольника и окружности
double difference(double a, double b, double c) {
  double p = (a + b + c) / 2;
  double rout, tr, diff;

  tr = sqrt((p - a) * (p - b) * (p - c) * p);
  rout = a * b * c / (sqrt(2 * p * (b + c - a) * (a + c - b) * (a + b - c)));
  diff = PI * rout * rout - tr;
  return diff;
}

void maxcords(cords_t answer[ANS], double *xmax, double *ymax) {
  *xmax = answer[0].xc;
  *ymax = answer[0].yc;

  for (int i = 1; i < ANS; i++) {
    if (answer[i].xc > *xmax)
      *xmax = (answer[i].xc);
    if (answer[i].yc > *ymax)
      *ymax = (answer[i].yc);
  }
}

void mincords(cords_t answer[ANS], double *xmin, double *ymin) {
  *xmin = answer[0].xc;
  *ymin = answer[0].yc;

  for (int i = 1; i < ANS; i++) {
    if (answer[i].xc < *xmin)
      *xmin = (answer[i].xc);
    if (answer[i].yc < *ymin)
      *ymin = (answer[i].yc);
  }
}
