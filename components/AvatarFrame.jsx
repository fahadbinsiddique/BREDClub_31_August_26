import React from 'react';

/**
 * AvatarFrame - Reusable committee member avatar component
 * Designed for background-removed (transparent PNG) images
 * Prevents head clipping with object-contain + top padding
 *
 * @param {string} name - Member full name
 * @param {string} designation - Member role/title
 * @param {string} photo - URL to profile image (transparent PNG preferred)
 */
const AvatarFrame = ({ name, designation, photo }) => {
  const initials = name
    ?.split(' ')
    .map((w) => w[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();

  return (
    <div className="text-center p-6 bg-white rounded-2xl shadow-[0_1px_3px_rgba(0,0,0,0.08)] border border-gray-200 hover:-translate-y-1.5 transition-transform duration-300">
      {/* ── Avatar Container ── */}
      <div className="relative w-48 h-48 md:w-56 md:h-56 mx-auto rounded-full overflow-hidden bg-[#0A5C36] shadow-[0_4px_20px_rgba(10,92,54,0.3)]">
        {/* Profile Image - z-10, padded from top to prevent head clipping */}
        {photo ? (
          <img
            src={photo}
            alt={name}
            className="absolute inset-0 w-full h-full object-contain object-bottom z-10 pt-3"
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center text-white text-4xl font-bold z-10 select-none">
            {initials}
          </div>
        )}

        {/* Bottom Wave Graphic - z-20 */}
        <svg
          className="absolute bottom-0 left-0 w-full z-20"
          style={{ height: '30%' }}
          viewBox="0 0 200 60"
          preserveAspectRatio="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M0,32 C35,56 55,12 100,36 C145,60 165,16 200,38 L200,60 L0,60 Z"
            fill="#E89B27"
          />
        </svg>

        {/* Brand Watermark - z-30 */}
        <span className="absolute bottom-2 left-1/2 -translate-x-1/2 text-white text-[10px] font-bold tracking-[3px] z-30 drop-shadow-md select-none">
          BRED
        </span>
      </div>

      {/* ── Member Info ── */}
      <h3 className="text-xl font-bold text-gray-900 mt-4 text-center leading-tight">
        {name}
      </h3>
      <p className="text-xs md:text-sm font-semibold tracking-wider text-[#0A5C36] mt-1 text-center uppercase">
        {designation}
      </p>
    </div>
  );
};

export default AvatarFrame;
