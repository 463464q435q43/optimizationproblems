/* s26 independent n-first Arb source weights and exact rough-log bins. */
#include <flint/arb.h>
#include <flint/arf.h>
#include <flint/fmpz.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>
#define N 690988
#define PREC 192
#define NB 320
static arb_ptr amp;
static int *rr,*om;
static int pp[4]={2,3,5,7};
static void bounds(FILE*f,const arb_t v,int bits){
 arb_t z;arb_init(z);arb_mul_2exp_si(z,v,bits);arf_t a;arf_init(a);fmpz_t l,h;fmpz_init(l);fmpz_init(h);
 arb_get_lbound_arf(a,z,PREC);arf_get_fmpz(l,a,ARF_RND_FLOOR);arb_get_ubound_arf(a,z,PREC);arf_get_fmpz(h,a,ARF_RND_CEIL);
 fmpz_fprint(f,l);fputc(' ',f);fmpz_fprint(f,h);fputc('\n',f);arb_clear(z);arf_clear(a);fmpz_clear(l);fmpz_clear(h);
}
static void dec(FILE*f,const char*name,const arb_t v){
 arb_t z;arb_init(z);arb_mul_ui(z,v,1000000000000UL,PREC);arf_t a;arf_init(a);fmpz_t l,h;fmpz_init(l);fmpz_init(h);
 arb_get_lbound_arf(a,z,PREC);arf_get_fmpz(l,a,ARF_RND_FLOOR);arb_get_ubound_arf(a,z,PREC);arf_get_fmpz(h,a,ARF_RND_CEIL);
 fprintf(f,"%s ",name);fmpz_fprint(f,l);fputc(' ',f);fmpz_fprint(f,h);fputc('\n',f);arb_clear(z);arf_clear(a);fmpz_clear(l);fmpz_clear(h);
}
static void amplitudes(int num,int den){
 arb_t x,c,t,l,z,q,pi;arb_init(x);arb_init(c);arb_init(t);arb_init(l);arb_init(z);arb_init(q);arb_init(pi);
 arb_set_str(x,"6000000185827",PREC);arb_mul(q,x,x,PREC);arb_add_ui(q,q,1,PREC);arb_sqrt(c,q,PREC);arb_const_pi(pi,PREC);arb_mul_ui(pi,pi,4,PREC);arb_div(c,c,pi,PREC);arb_log(c,c,PREC);arb_div_ui(c,c,4,PREC);arb_inv(q,q,PREC);arb_div_ui(q,q,2,PREC);arb_sub(c,c,q,PREC);arb_set_si(t,num);arb_div_ui(t,t,den,PREC);
 for(int n=1;n<=N;n++){arb_set_ui(l,n);arb_log(l,l,PREC);arb_mul(z,l,l,PREC);arb_div_ui(z,z,4,PREC);arb_mul(q,c,l,PREC);arb_sub(z,z,q,PREC);arb_mul(z,z,t,PREC);arb_div_ui(q,l,2,PREC);arb_sub(z,z,q,PREC);arb_exp(amp+n,z,PREC);}
 arb_clear(x);arb_clear(c);arb_clear(t);arb_clear(l);arb_clear(z);arb_clear(q);arb_clear(pi);
}
int main(void){
 flint_set_num_threads(1);rr=calloc(N+1,sizeof(int));om=calloc(N+1,sizeof(int));amp=_arb_vec_init(N+1);int ns=0;
 for(int n=1;n<=N;n++){int r=n;for(int j=0;j<4;j++)while(r%pp[j]==0){r/=pp[j];om[n]++;}rr[n]=r;if(r==1)ns++;}assert(ns==1160);
 FILE*sum=fopen("p_summary.txt","w");assert(sum);arb_t a,b,z,W,cp,cm,vs;arb_init(a);arb_init(b);arb_init(z);arb_init(W);arb_init(cp);arb_init(cm);arb_init(vs);
 amplitudes(13,80);for(int n=1;n<=N;n++){arb_add(b,b,amp+n,PREC);if(rr[n]==1)arb_add(a,a,amp+n,PREC);}arb_mul_ui(a,a,2,PREC);arb_sub(a,a,b,PREC);dec(sum,"anchor745",a);
 amplitudes(4,25);FILE*raw=fopen("p_raw.txt","w");for(int n=1;n<=N;n++){fprintf(raw,"%d ",n);bounds(raw,amp+n,56);}fclose(raw);
 arb_ptr plus=_arb_vec_init(N+1),minus=_arb_vec_init(N+1),bins=_arb_vec_init(NB);int counts[NB]={0},lo[NB]={0},hi[NB]={0};uint64_t rsum[NB]={0};
 for(int n=1;n<=N;n++){arb_add(plus+rr[n],plus+rr[n],amp+n,PREC);if(om[n]&1)arb_sub(minus+rr[n],minus+rr[n],amp+n,PREC);else arb_add(minus+rr[n],minus+rr[n],amp+n,PREC);}
 arb_set(cp,plus+1);arb_set(cm,minus+1);assert(arb_is_positive(cp)&&arb_is_positive(cm));
 arb_inv(a,cp,PREC);arb_mul(a,a,a,PREC);arb_mul_ui(a,a,8,PREC);arb_inv(b,cm,PREC);arb_mul(b,b,b,PREC);arb_add(a,a,b,PREC);arb_div_ui(a,a,900,PREC);arb_sqrt(vs,a,PREC);assert(arb_is_positive(vs));arb_set(W,vs);
 FILE*wf=fopen("p_weights.txt","w");fprintf(wf,"0 ");bounds(wf,vs,56);int nr=0;
 for(int r=2;r<=N;r++)if(rr[r]==r){nr++;arb_div(a,plus+r,cp,PREC);arb_mul(a,a,a,PREC);arb_mul_ui(a,a,8,PREC);arb_div(b,minus+r,cm,PREC);arb_mul(b,b,b,PREC);arb_add(a,a,b,PREC);arb_div_ui(a,a,9,PREC);arb_sqrt(z,a,PREC);assert(arb_is_positive(z));arb_add(W,W,z,PREC);
  fprintf(wf,"%d ",r);bounds(wf,z,56);
  int e=0;while((1<<(e+1))<=r)e++;int k=(16*r)/(1<<e)-16;int ix=16*e+k;assert(ix<NB&&k>=0&&k<16);if(!counts[ix])lo[ix]=r;hi[ix]=r;counts[ix]++;rsum[ix]+=r;arb_add(bins+ix,bins+ix,z,PREC);
 }assert(nr==157939);fclose(wf);
 dec(sum,"core_plus",cp);dec(sum,"core_minus",cm);dec(sum,"weight_sum",W);dec(sum,"synthetic_v",vs);fclose(sum);
 FILE*f=fopen("p_bins.txt","w");fprintf(f,"-1 0 0 0 0 ");bounds(f,vs,100);
 int ng=0;for(int j=0;j<NB;j++)if(counts[j]){ng++;fprintf(f,"%d %d %d %d %llu ",j,lo[j],hi[j],counts[j],(unsigned long long)rsum[j]);bounds(f,bins+j,100);}fclose(f);
 printf("PRIMARY COMPLETE source_N=%d smooth=%d rough=%d bins=%d\n",N,ns,nr,ng);return 0;
}
