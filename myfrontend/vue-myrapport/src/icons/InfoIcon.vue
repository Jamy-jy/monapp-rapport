<template>
    <svg class="w-10 h-10 text-white icon" viewBox="0 0 52 52" fill="none">
        <circle class="circle" cx="26" cy="26" r="24"/>
        <path class="line" d="M26 23V34"/>
        <circle class="dot" cx="26" cy="17" r="2"/>
    </svg>
</template>

<style scoped>
    .icon{
        animation:pop .4s ease;
    }

    circle,
    path{
        stroke:currentColor;
        stroke-width:3;
        stroke-linecap:round;
        fill:none;
    }

    .circle{
        stroke-dasharray:166;
        stroke-dashoffset:166;
        animation:draw .55s forwards;
    }

    .line{
        stroke-dasharray:14;
        stroke-dashoffset:14;
        animation:draw .25s .45s forwards;
    }

    .dot{
        opacity:0;
        animation:show .2s .65s forwards;
    }

    @keyframes draw{
        to{
            stroke-dashoffset:0;
        }
    }

    @keyframes show{
        to{
            opacity:1;
        }
    }

    @keyframes pop{
        0%{
            transform:scale(.6);
            opacity:0;
        }
        100%{
            transform:scale(1);
            opacity:1;
        }
    }
</style>