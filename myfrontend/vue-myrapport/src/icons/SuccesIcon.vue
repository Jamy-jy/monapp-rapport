<template>
    <svg
        class="w-10 h-10 text-white success-icon"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
    >
        <rect class="box" x="4" y="4" width="16" height="16" rx="2"/>
        <path class="check" d="M9 12l2 2l4-4"/>
    </svg>
</template>
<style scoped>
    .success-icon{
    animation: pop .35s ease;
    }

    .box{
    stroke-dasharray:64;
    stroke-dashoffset:64;
    animation: draw .5s ease forwards;
    }

    .check{
    stroke-dasharray:12;
    stroke-dashoffset:12;
    animation:
    draw .4s ease forwards .35s;
    }

    @keyframes draw{
    to{
    stroke-dashoffset:0;
    }
    }

    @keyframes pop{
    0%{
    transform:scale(.5);
    opacity:0;
    }
    70%{
    transform:scale(1.1);
    }
    100%{
    transform:scale(1);
    opacity:1;
    }
    }
</style>