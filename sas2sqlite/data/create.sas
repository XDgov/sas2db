/* based on https://documentation.sas.com/?docsetId=lrcon&docsetTarget=n1xrpfyevzkdaen1m1meb5z8qwc6.htm&docsetVersion=9.4&locale=en#p1gvdtdxd20j2xn1dqukmnsc3c1b */
Libname out '/folders/myfolders';

data investment;
    begin='01JAN1990'd;
    format enddate e8601dn.;
    enddate='31DEC2009'd;
    label Info="Just some characters";
    length year 4;

    do year=year(begin) to year(enddate);
        Capital+2000 + .07*(Capital+2000);
        YearFormatted=year;
        Info="Random characters for year "||year;
        output;
    end;
    put 'The number of DATA step iterations is '_n_;
run;

proc print data=investment;
    format Capital dollar12.2;
run;

data out.example;
    Set investment;
Run;